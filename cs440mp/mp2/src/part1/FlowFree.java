package part1;

import java.io.IOException;
import java.math.BigInteger;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;
import java.util.List;
import java.util.function.Function;
import java.util.stream.Collectors;

public class FlowFree {

    private HashSet<Character> domain = new HashSet<>();
    private int width, height;
    private ColorCell[][] board;
    private int remaining = 0;
    private long elapsedTime = 0;
    private BigInteger attempt = BigInteger.ZERO;

    public FlowFree(String input) {
        String[] lines = input.split("\n");
        height = lines.length;
        width = lines[0].trim().length();
        board = new ColorCell[height][width];
        for (int i = 0; i < height; i++) {
            for (int j = 0; j < width; j++) {
                char c = lines[i].charAt(j);
                if (c != '\n') {
                    if (c >= 'A' && c <= 'Z' || c >= 'a' && c <= 'z') {
                        if (!domain.contains(c))
                            domain.add(c);
                        board[i][j] = new ColorCell(c, i, j, this);
                    } else if (c == '_') {
                        board[i][j] = new ColorCell(i, j, this);
                        remaining++;
                    }
                }
            }
        }
        for (int i = 0; i < height; i++) {
            for (int j = 0; j < width; j++) {
                if (!board[i][j].isAssigned()) {
                    ArrayList<Character> tmp = new ArrayList<>();
                    for (char c : domain)
                        tmp.add(c);
                    board[i][j].setDomain(tmp);

                    if (i - 1 >= 0)
                        board[i - 1][j].incrementUnAssignedNeighbor();
                    if (i + 1 < height)
                        board[i + 1][j].incrementUnAssignedNeighbor();
                    if (j - 1 >= 0)
                        board[i][j - 1].incrementUnAssignedNeighbor();
                    if (j + 1 < width)
                        board[i][j + 1].incrementUnAssignedNeighbor();
                } else {
                    if (i - 1 >= 0)
                        board[i - 1][j].incrementAssignedNeighbor();
                    if (i + 1 < height)
                        board[i + 1][j].incrementAssignedNeighbor();
                    if (j - 1 >= 0)
                        board[i][j - 1].incrementAssignedNeighbor();
                    if (j + 1 < width)
                        board[i][j + 1].incrementAssignedNeighbor();
                }
            }
        }
    }

    public int getWidth() {
        return width;
    }

    public int getHeight() {
        return height;
    }

    public HashSet<Character> getDomain() {
        return domain;
    }

    public BigInteger getAttempt() {
        return attempt;
    }

    public boolean consistent() {
        for (int i = 0; i < height; i++) {
            for (int j = 0; j < width; j++) {
                if (!cellConsistent(i, j))
                    return false;
            }
        }
        return true;
    }

    private boolean cellConsistent(int r, int c) {
        ColorCell cell = board[r][c];
        if (!cell.isAssigned())
            return true;
        char color = cell.getColor();

        int consistentColorCount = 0;
        int neighborAssignedCount = 0;
        int neighborUnAssignedCount = 0;
        if (r - 1 >= 0) {
            if (board[r - 1][c].isAssigned()) {
                neighborAssignedCount++;
                if (board[r - 1][c].getColor() == color)
                    consistentColorCount++;
            } else {
                neighborUnAssignedCount++;
            }
        }
        if (r + 1 < height) {
            if (board[r + 1][c].isAssigned()) {
                neighborAssignedCount++;
                if (board[r + 1][c].getColor() == color)
                    consistentColorCount++;
            } else {
                neighborUnAssignedCount++;
            }
        }
        if (c - 1 >= 0) {
            if (board[r][c - 1].isAssigned()) {
                neighborAssignedCount++;
                if (board[r][c - 1].getColor() == color)
                    consistentColorCount++;
            } else {
                neighborUnAssignedCount++;
            }
        }
        if (c + 1 < width) {
            if (board[r][c + 1].isAssigned()) {
                neighborAssignedCount++;
                if (board[r][c + 1].getColor() == color)
                    consistentColorCount++;
            } else {
                neighborUnAssignedCount++;
            }
        }
        return neighborAssignedCount == 0 ||
                (cell.isNode() &&
                        (consistentColorCount == 1 ||
                                (neighborUnAssignedCount != 0 && consistentColorCount + neighborUnAssignedCount >= 1))) ||
                (!cell.isNode() &&
                        (consistentColorCount == 2 ||
                                (neighborUnAssignedCount != 0 && consistentColorCount + neighborUnAssignedCount >= 2)));
    }

    //select next var to assign
    //choose the one with the least number of outpaths(most number of neighbors including boundaries)
    private ColorCell selectNextCell() {
        int max_assigned_neighbor = 0;
        int max_unassigned_neighbor = 0;
        int next_i = -1;
        int next_j = -1;
        for (int i = 0; i < height; i++) {
            for (int j = 0; j < width; j++) {
                if (!board[i][j].isAssigned()) {
                    int assigned_neighbor = board[i][j].getAssignedNeighbor();
                    int unassigned_neighbor = board[i][j].getUnAssignedNeighbor();

                    if (i == 0 || i == height - 1) assigned_neighbor++;
                    if (j == 0 || j == width - 1) assigned_neighbor++;

                    if (assigned_neighbor > max_assigned_neighbor) {
                        max_assigned_neighbor = assigned_neighbor;
                        next_i = i;
                        next_j = j;
                    } else if (assigned_neighbor == max_assigned_neighbor &&
                            unassigned_neighbor > max_unassigned_neighbor) {
                        max_unassigned_neighbor = unassigned_neighbor;
                        next_i = i;
                        next_j = j;
                    }
                }
            }
        }
        if (next_i == -1 || next_j == -1) {
            throw new Error("No more unassigned variable");
        }
        return board[next_i][next_j];
    }

    //rearrange the order of values in domain to assign
    //put the color in the most number of neighbors first
    private HashMap<Character, Integer> hm = new HashMap<>();

    private void rearrangeDomain(ColorCell cell) {
        int cell_x = cell.getRow();
        int cell_y = cell.getCol();
        ArrayList<Character> domain = cell.getDomain();
        hm.clear();
        for (char color : domain)
            hm.put(color, 0);

        if (cell_x - 1 >= 0 && !board[cell_x - 1][cell_y].isAssigned()) {
            ArrayList<Character> tmpDomain = board[cell_x - 1][cell_y].getDomain();
            for (char color : tmpDomain)
                if (hm.containsKey(color))
                    hm.put(color, hm.get(color) + 1);
        }
        if (cell_x + 1 < height && !board[cell_x + 1][cell_y].isAssigned()) {
            ArrayList<Character> tmpDomain = board[cell_x + 1][cell_y].getDomain();
            for (char color : tmpDomain)
                if (hm.containsKey(color))
                    hm.put(color, hm.get(color) + 1);
        }
        if (cell_y - 1 >= 0 && !board[cell_x][cell_y - 1].isAssigned()) {
            ArrayList<Character> tmpDomain = board[cell_x][cell_y - 1].getDomain();
            for (char color : tmpDomain)
                if (hm.containsKey(color))
                    hm.put(color, hm.get(color) + 1);
        }
        if (cell_y + 1 < width && !board[cell_x][cell_y + 1].isAssigned()) {
            ArrayList<Character> tmpDomain = board[cell_x][cell_y + 1].getDomain();
            for (char color : tmpDomain)
                if (hm.containsKey(color))
                    hm.put(color, hm.get(color) + 1);
        }

        cell.setDomain(hm.entrySet().stream()
                .sorted((e1, e2) -> e1.getValue() == 2 ? 1 : e2.getValue().compareTo(e1.getValue()))
                .map(Map.Entry::getKey)
                .collect(Collectors.toList()));
    }

    private boolean forward_checking() {
        for (int i = 0; i < height - 1; i++) {
            for (int j = 0; j < width - 1; j++) {
                if (board[i][j].isAssigned()
                        && board[i + 1][j].isAssigned()
                        && board[i][j + 1].isAssigned()
                        && board[i + 1][j + 1].isAssigned()
                        && board[i][j].getColor() == board[i + 1][j].getColor()
                        && board[i][j].getColor() == board[i][j + 1].getColor()
                        && board[i][j].getColor() == board[i + 1][j + 1].getColor()) {
                    return false;
                }
            }
        }
        return true;
    }

    public boolean backtracking_random() {
        final long startTime = System.currentTimeMillis();
        final int[] hr = new Random().ints(0, height).distinct().limit(height).toArray();
        final int[] wr = new Random().ints(0, width).distinct().limit(width).toArray();
        boolean ret = backtracking(remaining,
                (Void) -> {
                    for (int i = 0; i < height; i++)
                        for (int j = 0; j < width; j++)
                            if (!board[hr[i]][wr[j]].isAssigned()) return board[hr[i]][wr[j]];
                    throw new Error("No more unassigned variable");
                },
                (cell) -> {
                    ArrayList<Character> domain = cell.getDomain();
                    Collections.shuffle(domain);
                    return null;
                },
                (Void) -> true);
        final long endTime = System.currentTimeMillis();
        elapsedTime = endTime - startTime;
        return ret;
    }

    public boolean backtracking_smart() {
        final long startTime = System.currentTimeMillis();
        boolean ret = backtracking(remaining,
                (Void) -> selectNextCell(),
                (cell) -> {
                    rearrangeDomain(cell);
                    return null;
                },
                (Void) -> true);
        final long endTime = System.currentTimeMillis();
        elapsedTime = endTime - startTime;
        return ret;
    }

    public boolean backtracking_smarter() {
        final long startTime = System.currentTimeMillis();
        boolean ret = backtracking(remaining,
                (Void) -> selectNextCell(),
                (cell) -> {
                    rearrangeDomain(cell);
                    return null;
                },
                (Void) -> forward_checking()
        );
        final long endTime = System.currentTimeMillis();
        elapsedTime = endTime - startTime;
        return ret;
    }

    private boolean backtracking(int remain,
                                 Function<Void, ColorCell> selectVar,
                                 Function<ColorCell, Void> selectVal,
                                 Function<Void, Boolean> earlyDetect) {
        if (remain == 0) return true;
        ColorCell cell = selectVar.apply(null);
        selectVal.apply(cell);
        List<Character> domain = cell.getDomain();
        for (int i = 0; i < domain.size(); i++) {
            char color = domain.get(i);
            cell.assign(color);
            attempt = attempt.add(BigInteger.ONE);
            if (
                    earlyDetect.apply(null) &&
                            consistent() &&
                            backtracking(remain - 1, selectVar, selectVal, earlyDetect)) {
                return true;
            }
            cell.unassign();
        }
        return false;
    }

    public ColorCell[][] getBoard() {
        return board;
    }

    public ColorCell getCell(int r, int c) {
        return board[r][c];
    }

    public long getElapsedTime() {
        return elapsedTime;
    }

    @Override
    public String toString() {
        StringBuilder ret = new StringBuilder();
        for (int i = 0; i < height; i++) {
            for (int j = 0; j < width; j++) {
                String tmp = "";
                if (board[i][j].isAssigned())
                    ret.append(board[i][j].getColor() + tmp);
                else
                    ret.append("_" + tmp);
            }
            ret.append("\n");
        }
        return ret.toString();
    }

    public static void main(String[] args) {
        try {
            String input = new String(Files.readAllBytes(Paths.get("inputs/input1214.txt").toAbsolutePath()));
            FlowFree flowFree = new FlowFree(input);
            flowFree.backtracking_smarter();
            new FlowFreeGui(flowFree);
            System.out.println(flowFree);
            System.out.println("Solution found in " + flowFree.getElapsedTime() + "ms. " + flowFree.getAttempt() + " attempts.");
        } catch (IOException e) {
            System.err.println("File not read.");
        }
    }
}
