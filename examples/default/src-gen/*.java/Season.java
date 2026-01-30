import java.util.List;
import java.util.ArrayList;

public class Season {

    private List<Match> includes;

    public Season() {
        this.includes = new ArrayList<>();
    }

    public List<Match> getIncludes() {
        return this.includes;
    }

    public void setIncludes(List<Match> includes) {
        this.includes = includes;
    }

}