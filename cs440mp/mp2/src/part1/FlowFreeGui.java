package part1;

import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.util.HashMap;
import java.util.HashSet;

public class FlowFreeGui extends JFrame {
    private static int SIZE = 50;
    private HashMap<Character, Color> colorMap = new HashMap<>();

    private class FlowFreePanel extends JPanel {
        private FlowFree flowFree;
        private HashSet<Character> domain;

        public FlowFreePanel(FlowFree flowFree) {
            this.flowFree = flowFree;
            this.domain = flowFree.getDomain();
            float increment = (float) (1.0 / this.domain.size());
            int i = 0;
            for (char color : domain) {
                colorMap.put(color, Color.getHSBColor(i * increment, 1, 1));
                i++;
            }
            colorMap.put('?', Color.WHITE);
        }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            Graphics2D g2 = (Graphics2D) g.create();
            ColorCell[][] board = flowFree.getBoard();
            boolean[][] checked = new boolean[flowFree.getHeight()][flowFree.getWidth()];
            for (int i = 0; i < flowFree.getHeight(); i++) {
                for (int j = 0; j < flowFree.getWidth(); j++) {
                    g2.setColor(colorMap.get(board[i][j].getColor()).darker().darker().darker());
                    g2.fillRect(j * SIZE, i * SIZE, SIZE, SIZE);
                    g2.setColor(Color.GRAY);
                    g2.drawRect(j * SIZE, i * SIZE, SIZE, SIZE);
                }
            }

            for (int i = 0; i < flowFree.getHeight(); i++) {
                for (int j = 0; j < flowFree.getWidth(); j++) {
                    ColorCell cell = board[i][j];
                    if (!checked[i][j] && cell.isNode())
                        DFSDraw(-1, -1, i, j, flowFree.getHeight(), flowFree.getWidth(), board, checked, g2);
                }
            }
        }

        private void DFSDraw(int pi, int pj, int i, int j, int h, int w, ColorCell[][] board, boolean[][] checked, Graphics2D g) {
            checked[i][j] = true;
            g.setColor(colorMap.get(board[i][j].getColor()));
            if (board[i][j].isNode()) {
                g.fillOval(j * SIZE + SIZE / 2 - 13, i * SIZE + SIZE / 2 - 13, 26, 26);
            }
            if (pi != -1 && pj != -1) {
                g.setStroke(new BasicStroke(11, BasicStroke.CAP_ROUND, BasicStroke.JOIN_BEVEL));
                g.drawLine(pj * SIZE + SIZE / 2, pi * SIZE + SIZE / 2, j * SIZE + SIZE / 2, i * SIZE + SIZE / 2);
            }
            if (i - 1 >= 0 && !checked[i - 1][j] && board[i][j].getColor() == board[i - 1][j].getColor())
                DFSDraw(i, j, i - 1, j, h, w, board, checked, g);
            if (i + 1 < h && !checked[i + 1][j] && board[i][j].getColor() == board[i + 1][j].getColor())
                DFSDraw(i, j, i + 1, j, h, w, board, checked, g);
            if (j - 1 >= 0 && !checked[i][j - 1] && board[i][j].getColor() == board[i][j - 1].getColor())
                DFSDraw(i, j, i, j - 1, h, w, board, checked, g);
            if (j + 1 < w && !checked[i][j + 1] && board[i][j].getColor() == board[i][j + 1].getColor())
                DFSDraw(i, j, i, j + 1, h, w, board, checked, g);
        }

        @Override
        public Dimension getPreferredSize() {
            return new Dimension(flowFree.getWidth() * SIZE, flowFree.getHeight() * SIZE);
        }
    }

    public FlowFreeGui(FlowFree flowFree) {
        setTitle("Flow Free");
        setResizable(false);
        setLayout(new BorderLayout());
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        add(new FlowFreePanel(flowFree), BorderLayout.CENTER);
        pack();
        setVisible(true);
    }
}
