import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.text.SimpleDateFormat;
import java.util.Date;

//TODO:
// 1. change time format to unix time stamp and absolute time

// 2. Add keyboard shortcuts to the buttons


public class TallyCounter extends JFrame implements ActionListener {
    private int count;
    private JLabel countLabel;
    private JButton plusButton;
    private JButton minusButton;
    private String filename = "count_history.csv";

    public TallyCounter() {
        // Initialize the GUI components
        count = 0;
        countLabel = new JLabel("0");
        plusButton = new JButton("+");
        minusButton = new JButton("-");
        plusButton.addActionListener(this);
        minusButton.addActionListener(this);
        
        // Add keyboard shortcuts to the buttons
        plusButton.getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW).put(KeyStroke.getKeyStroke(KeyEvent.VK_EQUALS, KeyEvent.SHIFT_DOWN_MASK), "plus");
        plusButton.getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW).put(KeyStroke.getKeyStroke(KeyEvent.VK_PLUS, KeyEvent.SHIFT_DOWN_MASK), "plus");
        plusButton.getActionMap().put("plus", new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                plusButton.doClick();
            }
        });
        minusButton.getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW).put(KeyStroke.getKeyStroke(KeyEvent.VK_MINUS, 0), "minus");
        minusButton.getActionMap().put("minus", new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                minusButton.doClick();
            }
        });
        
        // Add the GUI components to the frame
        JPanel panel = new JPanel(new GridLayout(1, 3));
        panel.add(minusButton);
        panel.add(countLabel);
        panel.add(plusButton);
        getContentPane().add(panel);
        
        // Set up the frame
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setTitle("Tally Counter");
        pack();
        setVisible(true);
    }
    
    public void actionPerformed(ActionEvent e) {
        // Handle button clicks
        if (e.getSource() == plusButton) {
            count++;
        } else if (e.getSource() == minusButton) {
            count--;
        }
        countLabel.setText(Integer.toString(count));
        
        // Save the current count and time to CSV
        try (FileWriter writer = new FileWriter(filename, true)) {
            SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            String timestamp = dateFormat.format(new Date());
            writer.write(count + "," + timestamp + "\n");
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }

    public static void main(String[] args) {
        new TallyCounter();
    }
}
