import java.util.List;
import java.util.ArrayList;

public class SoccerTeam {

    private List<Player> has;
    private Coach employs;
    private Stadium homeGround;

    public SoccerTeam() {
        this.has = new ArrayList<>();
    }

    public List<Player> getHas() {
        return this.has;
    }

    public void setHas(List<Player> has) {
        this.has = has;
    }

    public Coach getEmploys() {
        return this.employs;
    }

    public void setEmploys(Coach employs) {
        this.employs = employs;
    }

    public Stadium getHomeGround() {
        return this.homeGround;
    }

    public void setHomeGround(Stadium homeGround) {
        this.homeGround = homeGround;
    }

}