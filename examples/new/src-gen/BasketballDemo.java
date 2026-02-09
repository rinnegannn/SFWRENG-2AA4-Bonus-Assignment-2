/**
 * This is a proof of concept demo for the basketball system model and algorithm.
 * This demo shows the usage of the generated Java classes from the basketball model.
 * It creates instances of various classes, sets their attributes, and establishes relationships between them.
 * Lastly, it prints out a summary of the created objects and their relationships.
 */

public class BasketballDemo {
    public static void main(String[] args) {
        System.out.println("Basketball Model System Demo\n");

        //create conference and team
        Conference nbaWest = new Conference();
        BasketballTeam raptors = new BasketballTeam();
        
        //generated list getter to add team to conference (includes 1:*)
        nbaWest.getIncludes().add(raptors);
        System.out.println("Created new Conference and added Toronto Raptors.");

        //create home court (home_court *:1)
        Arena scotiabankArena = new Arena();
        raptors.setHomeCourt(scotiabankArena);
        System.out.println("Set Scotiabank Arena as home court for Raptors.");

        //coaching (led_by 1:1)
        HeadCoach Steve = new HeadCoach();
        raptors.setLedBy(Steve); 
        System.out.println("Assigned Head Coach to the team.");

        //create roster (roster 1:*)
        BasketballPlayer LaMelo = new BasketballPlayer();
        BasketballPlayer Curry = new BasketballPlayer();
        
        //initializes 'roster' as an ArrayList
        raptors.getRoster().add(LaMelo);
        raptors.getRoster().add(Curry);
        System.out.println("Added " + raptors.getRoster().size() + " players to the roster.");
        //create game and assign teams (competes 1:2)
        Game game = new Game();
        BasketballTeam warriors = new BasketballTeam();
        //generator creates an array BasketballTeam[] since competes is 1:2
        game.setCompetes(new BasketballTeam[]{raptors, warriors});
        game.setHostedAt(scotiabankArena);
        System.out.println("New game created at " + game.getHostedAt().getClass().getSimpleName());

        //record scores (made_by *:1 and during *:1)
        Basket threePointer = new Basket();
        threePointer.setMadeBy(LaMelo); 
        threePointer.setDuring(game);   
        System.out.println("Recorded a basket made by Scottie during the game.");

        System.out.println("\nSummary:");
        System.out.println("Total teams in conference: " + nbaWest.getIncludes().size());
        System.out.println("Total players in Raptors roster: " + raptors.getRoster().size());
    }
}