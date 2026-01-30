import java.util.List;
import java.util.ArrayList;

public class BasketballTeam {

    private List<BasketballPlayer> roster;
    private HeadCoach ledBy;
    private Arena homeCourt;

    public BasketballTeam() {
        this.roster = new ArrayList<>();
    }

    public List<BasketballPlayer> getRoster() {
        return this.roster;
    }

    public void setRoster(List<BasketballPlayer> roster) {
        this.roster = roster;
    }

    public HeadCoach getLedBy() {
        return this.ledBy;
    }

    public void setLedBy(HeadCoach ledBy) {
        this.ledBy = ledBy;
    }

    public Arena getHomeCourt() {
        return this.homeCourt;
    }

    public void setHomeCourt(Arena homeCourt) {
        this.homeCourt = homeCourt;
    }

}