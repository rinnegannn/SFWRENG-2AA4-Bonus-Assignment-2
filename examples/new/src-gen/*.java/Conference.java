import java.util.List;
import java.util.ArrayList;

public class Conference {

    private List<BasketballTeam> includes;

    public Conference() {
        this.includes = new ArrayList<>();
    }

    public List<BasketballTeam> getIncludes() {
        return this.includes;
    }

    public void setIncludes(List<BasketballTeam> includes) {
        this.includes = includes;
    }

}