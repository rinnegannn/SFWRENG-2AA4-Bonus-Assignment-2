import java.util.List;
import java.util.ArrayList;

public class League {

    private List<SoccerTeam> contains;
    private List<Season> organizes;

    public League() {
        this.contains = new ArrayList<>();
        this.organizes = new ArrayList<>();
    }

    public List<SoccerTeam> getContains() {
        return this.contains;
    }

    public void setContains(List<SoccerTeam> contains) {
        this.contains = contains;
    }

    public List<Season> getOrganizes() {
        return this.organizes;
    }

    public void setOrganizes(List<Season> organizes) {
        this.organizes = organizes;
    }

}