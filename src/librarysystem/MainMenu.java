package librarysystem;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JTextField;

/**
 *
 * @Person Acer
 */
public class MainMenu {

    ArrayList<Movie> listMovies = new ArrayList<Movie>();

    public MainMenu() {
        JFrame f = new JFrame("Main Menu");
        JButton add_movie = new JButton("Add Movies"); // creating instance of JButton for adding Movies
        add_movie.setBounds(100, 60, 120, 25);

        add_movie.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                addMovies();

            }
        });
        JButton view_movie = new JButton("View Movies"); // creating instance of JButton for view Movies
        view_movie.setBounds(220, 60, 120, 25);

        view_movie.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    JFrame g = new JFrame("Movies  Details");
                    String moviesDetail = "";

                    try {
                        Class.forName("com.mysql.jdbc.Driver");
                    } catch (ClassNotFoundException ex) {
                        Logger.getLogger(MainMenu.class.getName()).log(Level.SEVERE, null, ex);
                    }
                    Connection con = DriverManager.getConnection(
                            "jdbc:mysql://localhost:3306/library", "root", "root");
                    Statement stmt = con.createStatement();
                    String sqlSelect = "select * from movie order by title desc";
                    ResultSet rs = stmt.executeQuery(sqlSelect);
                    while (rs.next()) {
                        String currentMovie = "Title:" + rs.getString(4) + "\r\n Person:" + rs.getString(5) + "\r\n Publish Year:"
                                + rs.getInt(2) + "\r\n No of Rating:" + rs.getInt(3);
                        moviesDetail = moviesDetail + currentMovie + "\r\n";
                    }
                    JLabel l1;

                    l1 = new JLabel("<html><pre>" + moviesDetail + "</pre></html>");
                    l1.setBounds(0, 0, 600, 380);
                    g.add(l1);
                    g.setSize(400, 400);// 400 width and 500 height
                    g.setLayout(null);// using no layout managers
                    g.setVisible(true);// making the frame visible
                    g.setLocationRelativeTo(null);

                    /*else {
                        JOptionPane.showMessageDialog(null, "First enter movie details.");
                    }*/
                } catch (SQLException ex) {
                    Logger.getLogger(MainMenu.class.getName()).log(Level.SEVERE, null, ex);
                }

            }
        });

        JButton viewCountMovieByYear = new JButton("Movie Count By Year"); // creating instance of JButton for view Movies
        viewCountMovieByYear.setBounds(330, 60, 150, 25);
        viewCountMovieByYear.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    JFrame g = new JFrame("Movies count by year");
                    String moviesDetail = "";

                    try {
                        Class.forName("com.mysql.jdbc.Driver");
                    } catch (ClassNotFoundException ex) {
                        Logger.getLogger(MainMenu.class.getName()).log(Level.SEVERE, null, ex);
                    }
                    Connection con = DriverManager.getConnection(
                            "jdbc:mysql://localhost:3306/library", "root", "root");
                    Statement stmt = con.createStatement();
                    String sqlSelect = "select count(*) as countMovie, publishYear from movie group by publishYear ";
                    ResultSet rs = stmt.executeQuery(sqlSelect);
                    String heading = "Year      Count Of Movies  \r\n";
                    while (rs.next()) {

                        String currentMovie = rs.getString(2) + "     " + rs.getString(1);
                        moviesDetail = moviesDetail + currentMovie + "\r\n";
                    }
                    JLabel l1;

                    l1 = new JLabel("<html><pre>" + heading + moviesDetail + "</pre></html>");
                    l1.setBounds(0, 0, 600, 380);
                    g.add(l1);
                    g.setSize(400, 400);// 400 width and 500 height
                    g.setLayout(null);// using no layout managers
                    g.setVisible(true);// making the frame visible
                    g.setLocationRelativeTo(null);

                } catch (SQLException ex) {
                    Logger.getLogger(MainMenu.class.getName()).log(Level.SEVERE, null, ex);
                }

            }
        });

        JButton quitButton = new JButton("Quit"); // creating instance of JButton for view Movies
        quitButton.setBounds(460, 60, 120, 25);

        quitButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                System.exit(0);

            }
        });
        f.add(add_movie);
        f.add(view_movie);
        f.add(viewCountMovieByYear);
        f.add(quitButton);
        f.setSize(600, 200);// 400 width and 500 height
        f.setLayout(null);// using no layout managers
        f.setVisible(true);// making the frame visible
        f.setLocationRelativeTo(null);

    }

    public void addMovies() {
        JFrame g = new JFrame("Enter Movies  Details"); // Frame to enter Movies details
        // Create label
        JLabel l1, l2, l3, l4;
        l1 = new JLabel("Title"); // label 1 for title
        l1.setBounds(30, 15, 100, 30);

        l2 = new JLabel("Person"); // label 2 for Person
        l2.setBounds(30, 50, 100, 30);

        l3 = new JLabel("Publish Year"); // label 1 for year
        l3.setBounds(30, 85, 100, 30);

        l4 = new JLabel("Number of Rating"); // label 2 for Rating
        l4.setBounds(30, 120, 100, 30);

        // set text field for title
        JTextField F_title = new JTextField();
        F_title.setBounds(130, 15, 150, 30);

        // set text field for Person
        JTextField F_person = new JTextField();
        F_person.setBounds(130, 50, 150, 30);

        // set text field for Rating
        JTextField F_year = new JTextField();
        F_year.setBounds(130, 85, 150, 30);

        // set text field for year
        JTextField F_rating = new JTextField();
        F_rating.setBounds(130, 120, 150, 30);

        JButton create_but = new JButton("Add movie");// creating instance of JButton for Create
        create_but.setBounds(130, 180, 130, 25);// x axis, y axis, width, height

        create_but.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent e) {

                String title = F_title.getText();
                String person = F_person.getText();
                String year = F_year.getText();
                String rating = F_rating.getText();

                try {
                    int intYear = Integer.parseInt(year);
                    int Rating = Integer.parseInt(rating);
                    if (intYear > Calendar.getInstance().get(Calendar.YEAR)) {
                        JOptionPane.showMessageDialog(null, "Year value should not be greater than current year.");
                    } else if (intYear <= 0 || Rating <= 0) {
                        JOptionPane.showMessageDialog(null, "Value of year or page should not be less than zero.");
                    } else {

                        try {
                            Class.forName("com.mysql.jdbc.Driver");
                        } catch (ClassNotFoundException ex) {
                            Logger.getLogger(MainMenu.class.getName()).log(Level.SEVERE, null, ex);
                        }
                        Connection con = DriverManager.getConnection(
                                "jdbc:mysql://localhost:3306/library", "root", "root");
                        Statement stmt = con.createStatement();
                        String sqlSelect = "select count(*) from movie";
                        ResultSet rs = stmt.executeQuery(sqlSelect);
                        rs.next();
                        int movieID = rs.getInt(1) + 1;

                        String sqlInsert = "insert into movie values (" + movieID + "," + intYear + "," + Rating + ",'" + title + "','" + person + "')";
                        stmt.executeUpdate(sqlInsert);
                        con.close();

                        // Movie movie = new Movie(intYear, Rating, title, person);
                        //listmovies.add(movie);
                        JOptionPane.showMessageDialog(null, "Movie entered!");
                        g.dispose();
                    }

                } catch (NumberFormatException err) {
                    JOptionPane.showMessageDialog(null, "Value should be valid numeric entry.");
                } catch (SQLException ex) {
                    Logger.getLogger(MainMenu.class.getName()).log(Level.SEVERE, null, ex);
                }

            }

        });

        g.add(create_but);
        g.add(l1);
        g.add(l2);
        g.add(l3);
        g.add(l4);
        g.add(F_title);
        g.add(F_person);
        g.add(F_year);
        g.add(F_rating);
        g.setSize(350, 400);// 400 width and 500 height
        g.setLayout(null);// using no layout managers
        g.setVisible(true);// making the frame visible
        g.setLocationRelativeTo(null);
    }
}
