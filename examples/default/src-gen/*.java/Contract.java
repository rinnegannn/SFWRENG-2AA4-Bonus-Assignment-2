public class Contract {

    private Player binds;
    private SoccerTeam with;

    public Contract() {
    }

    public Player getBinds() {
        return this.binds;
    }

    public void setBinds(Player binds) {
        this.binds = binds;
    }

    public SoccerTeam getWith() {
        return this.with;
    }

    public void setWith(SoccerTeam with) {
        this.with = with;
    }

}