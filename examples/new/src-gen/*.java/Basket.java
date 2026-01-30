public class Basket {

    private BasketballPlayer madeBy;
    private Game during;

    public Basket() {
    }

    public BasketballPlayer getMadeBy() {
        return this.madeBy;
    }

    public void setMadeBy(BasketballPlayer madeBy) {
        this.madeBy = madeBy;
    }

    public Game getDuring() {
        return this.during;
    }

    public void setDuring(Game during) {
        this.during = during;
    }

}