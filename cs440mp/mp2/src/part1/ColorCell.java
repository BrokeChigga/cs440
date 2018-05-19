package part1;

import java.util.ArrayList;
import java.util.List;

public class ColorCell {
    private final int row;
    private final int col;
    private int assignedNeighbor = 0;
    private int unAssignedNeighbor = 0;
    private boolean isAssigned;
    private boolean isNode;
    private char color = '?';
    private ArrayList<Character> domain = new ArrayList<>();
    private final FlowFree parent;

    public ColorCell(int i, int j, FlowFree parent) {
        this.row = i;
        this.col = j;
        isAssigned = false;
        isNode = false;
        this.parent = parent;
    }

    public ColorCell(char color, int i, int j, FlowFree parent) {
        this.row = i;
        this.col = j;
        isAssigned = true;
        isNode = true;
        this.color = color;
        this.parent = parent;
        this.domain = null;

    }

    public int getRow() {
        return this.row;
    }

    public int getCol() {
        return this.col;
    }

    public int getAssignedNeighbor() {
        return assignedNeighbor;
    }

    public int getUnAssignedNeighbor() {
        return unAssignedNeighbor;
    }

    public void incrementAssignedNeighbor() {
        assignedNeighbor++;
    }

    public void incrementUnAssignedNeighbor() {
        unAssignedNeighbor++;
    }

    public void decrementAssignedNeighbor() {
        assignedNeighbor--;
    }

    public void decrementUnAssignedNeighbor() {
        unAssignedNeighbor--;
    }

    public boolean isAssigned() {
        return isAssigned;
    }

    public boolean isNode() {
        return isNode;
    }

    public char getColor() {
        return color;
    }

    public void assign(char color) {
        if (isNode) {
            throw new IllegalAccessError("Node cannot be assigned color.");
        }
        this.color = color;
        this.isAssigned = true;
        int width = parent.getWidth();
        int height = parent.getHeight();
        if (row - 1 >= 0) {
            parent.getCell(row - 1, col).incrementAssignedNeighbor();
            parent.getCell(row - 1, col).decrementUnAssignedNeighbor();
        }
        if (row + 1 < height) {
            parent.getCell(row + 1, col).incrementAssignedNeighbor();
            parent.getCell(row + 1, col).decrementUnAssignedNeighbor();
        }
        if (col - 1 >= 0) {
            parent.getCell(row, col - 1).incrementAssignedNeighbor();
            parent.getCell(row, col - 1).decrementUnAssignedNeighbor();
        }
        if (col + 1 < width) {
            parent.getCell(row, col + 1).incrementAssignedNeighbor();
            parent.getCell(row, col + 1).decrementUnAssignedNeighbor();
        }
    }

    public void setDomain(List<Character> domain) {
        if (isNode)
            throw new Error("Node's domain is fixed");
        this.domain = new ArrayList<>(domain);
    }

    public ArrayList<Character> getDomain() {
        return domain;
    }

    public void unassign() {
        this.color = '?';
        this.isAssigned = false;
        int width = parent.getWidth();
        int height = parent.getHeight();
        if (row - 1 >= 0) {
            parent.getCell(row - 1, col).decrementAssignedNeighbor();
            parent.getCell(row - 1, col).incrementUnAssignedNeighbor();
        }
        if (row + 1 < height) {
            parent.getCell(row + 1, col).decrementAssignedNeighbor();
            parent.getCell(row + 1, col).incrementUnAssignedNeighbor();
        }
        if (col - 1 >= 0) {
            parent.getCell(row, col - 1).decrementAssignedNeighbor();
            parent.getCell(row, col - 1).incrementUnAssignedNeighbor();
        }
        if (col + 1 < width) {
            parent.getCell(row, col + 1).decrementAssignedNeighbor();
            parent.getCell(row, col + 1).incrementUnAssignedNeighbor();
        }
    }
}
