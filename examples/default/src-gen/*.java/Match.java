public class Match {

    private SoccerTeam[] involves;
    private Referee officiatedBy;
    private Stadium playedAt;

    public Match() {
    }

    public SoccerTeam[] getInvolves() {
        return this.involves;
    }

    public void setInvolves(SoccerTeam[] involves) {
        this.involves = involves;
    }

    public Referee getOfficiatedBy() {
        return this.officiatedBy;
    }

    public void setOfficiatedBy(Referee officiatedBy) {
        this.officiatedBy = officiatedBy;
    }

    public Stadium getPlayedAt() {
        return this.playedAt;
    }

    public void setPlayedAt(Stadium playedAt) {
        this.playedAt = playedAt;
    }

}