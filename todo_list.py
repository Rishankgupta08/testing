This task is not possible as the developer has asked to create Java code but the primary file is in Python. However, I will provide the equivalent Java code for the given Python program.

```java
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class TodoList {
    private JFrame frame;
    private JLabel taskNumber;
    private JTextField newTask;
    private JButton addTask;
    private JButton deleteTask;
    private JButton saveTasks;
    private JButton loadTasks;
    private DefaultListModel<String> listModel;
    private JList<String> list;

    public TodoList() {
        frame = new JFrame("Todo List");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(new BorderLayout());

        taskNumber = new JLabel("Tasks: 0");
        frame.add(taskNumber, BorderLayout.NORTH);

        newTask = new JTextField(40);
        frame.add(newTask, BorderLayout.CENTER);

        JPanel panel = new JPanel();
        addTask = new JButton("Add task");
        addTask.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                addTaskToList();
            }
        });
        panel.add(addTask);

        deleteTask = new JButton("Delete task");
        deleteTask.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                deleteTaskFromList();
            }
        });
        panel.add(deleteTask);

        saveTasks = new JButton("Save tasks");
        saveTasks.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                saveTasksToFile();
            }
        });
        panel.add(saveTasks);

        loadTasks = new JButton("Load tasks");
        loadTasks.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                loadTasksFromFile();
            }
        });
        panel.add(loadTasks);

        frame.add(panel, BorderLayout.SOUTH);

        listModel = new DefaultListModel<>();
        list = new JList<>(listModel);
        frame.add(new JScrollPane(list), BorderLayout.EAST);

        frame.pack();
        frame.setVisible(true);
    }

    private void addTaskToList() {
        String task = newTask.getText();
        if (!task.isEmpty()) {
            listModel.addElement(task);
            newTask.setText("");
            taskNumber.setText("Tasks: " + listModel.getSize());
        }
    }

    private void deleteTaskFromList() {
        int selectedIndex = list.getSelectedIndex();
        if (selectedIndex != -1) {
            listModel.remove(selectedIndex);
            taskNumber.setText("Tasks: " + listModel.getSize());
        } else {
            JOptionPane.showMessageDialog(frame, "Select a task to delete", "Warning", JOptionPane.WARNING_MESSAGE);
        }
    }

    private void saveTasksToFile() {
        try (FileWriter writer = new FileWriter("tasks.txt")) {
            for (int i = 0; i < listModel.getSize(); i++) {
                writer.write(listModel.get(i) + "\n");
            }
            JOptionPane.showMessageDialog(frame, "Tasks saved to tasks.txt", "Info", JOptionPane.INFORMATION_MESSAGE);
        } catch (IOException e) {
            JOptionPane.showMessageDialog(frame, "Error saving tasks", "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void loadTasksFromFile() {
        try {
            List<String> tasks = Files.readAllLines(Paths.get("tasks.txt"));
            listModel.clear();
            for (String task : tasks) {
                listModel.addElement(task);
            }
            taskNumber.setText("Tasks: " + listModel.getSize());
        } catch (IOException e) {
            JOptionPane.showMessageDialog(frame, "No tasks.txt file found", "Warning", JOptionPane.WARNING_MESSAGE);
        }
    }

    public static void main(String[] args) {
        new TodoList();
    }
}
```