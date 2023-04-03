package librarysystem;

import java.util.Calendar;
import javax.swing.JOptionPane;

/**
 *
 * @author Acer
 */
public class Movie {

    Integer publishYear;
    Integer rating;
    String title;
    String person;

    public Movie(Integer cPublishYear, Integer crating, String cTitle, String cperson) {
        this.publishYear = cPublishYear;
        this.rating = crating;
        this.title = cTitle;
        this.person = cperson;
    }

    public int getPublishYear() {

        return publishYear;
    }

    public int getrating() {

        return rating;
    }

    public String getTitle() {

        return title;
    }

    public String getperson() {

        return person;
    }

    public void setPublishYear(int spublishYear) {
        int year = Calendar.getInstance().get(Calendar.YEAR);
        if (spublishYear <= 0 || spublishYear > year) {
            JOptionPane.showMessageDialog(null, "Year value should greater than zero and less than equal to current year.");
        } else {
            this.publishYear = spublishYear;
        }

    }

    public void setrating(int srating) {
        if (srating <= 0) {
            JOptionPane.showMessageDialog(null, "Pages cannot be negative value.");
        } else {
            this.rating = srating;
        }
    }

    public void setTitle(String sTitle) {

        this.title = sTitle;
    }

    public void setperson(String sperson) {

        this.person = sperson;
    }

    @Override
    public String toString() {
        String MovieDetails = "";
        MovieDetails = "Title: " + this.title + "\n" + "person: " + this.person + "\n"
                + "No of Pages: " + String.valueOf(this.rating) + "\n"
                + "Publish year:" + String.valueOf(this.publishYear);
        return MovieDetails;
    }
}
