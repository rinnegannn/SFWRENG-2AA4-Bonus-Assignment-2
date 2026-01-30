public class Goal {

    private Player scoredBy;
    private Match scoredIn;

    public Goal() {
    }

    public Player getScoredBy() {
        return this.scoredBy;
    }

    public void setScoredBy(Player scoredBy) {
        this.scoredBy = scoredBy;
    }

    public Match getScoredIn() {
        return this.scoredIn;
    }

    public void setScoredIn(Match scoredIn) {
        this.scoredIn = scoredIn;
    }

}