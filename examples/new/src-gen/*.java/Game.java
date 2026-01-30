public class Game {

    private BasketballTeam[] competes;
    private Arena hostedAt;

    public Game() {
    }

    public BasketballTeam[] getCompetes() {
        return this.competes;
    }

    public void setCompetes(BasketballTeam[] competes) {
        this.competes = competes;
    }

    public Arena getHostedAt() {
        return this.hostedAt;
    }

    public void setHostedAt(Arena hostedAt) {
        this.hostedAt = hostedAt;
    }

}