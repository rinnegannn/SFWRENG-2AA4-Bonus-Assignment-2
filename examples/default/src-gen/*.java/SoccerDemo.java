/**
 * This is a proof of concept demo for the soccer system model and algorithm.
 * This demo shows the usage of the generated Java classes from the soccer model with two teams (FC Bayern Munich and Arsenal).
 * It creates instances of various classes, sets their attributes, and establishes relationships between them.
 * Lastly, it prints out a summary of the created objects and their relationships.
 */
public class SoccerDemo {
    
    public static void main(String[] args) {
        System.out.println("Demo of soccer model system\n");
        
        League championsLeague = new League(); //create a soccer league
        System.out.println("Created Champions League");
        
        Stadium AllianzArena = new Stadium(); //create stadium
        System.out.println("Created Allianz Arena Stadium");
        
        SoccerTeam FCBayernMunich = new SoccerTeam(); //make team 1
        FCBayernMunich.setHomeGround(AllianzArena);
        System.out.println("Created FC Bayern Munich with home ground at Allianz Arena");
        

        SoccerTeam Arsenal = new SoccerTeam(); //make team 2
        Stadium Emirates = new Stadium();
        Arsenal.setHomeGround(Emirates);
        System.out.println("Created Arsenal with home ground at Emirates Stadium");
        
        Coach coach = new Coach(); //coach for team 1
        FCBayernMunich.setEmploys(coach);
        System.out.println("Assigned coach to FC Bayern Munich");
        
        //players for team 1 and add to team
        Player player1 = new Player();
        Player player2 = new Player();
        Player player3 = new Player();
        
        FCBayernMunich.getHas().add(player1);
        FCBayernMunich.getHas().add(player2);
        FCBayernMunich.getHas().add(player3);
        System.out.println("Added 3 players to FC Bayern Munich");
        
        //create a ref
        Referee referee = new Referee();
        System.out.println("Created a referee");
        

        //create a game
        Match match = new Match();
        match.setInvolves(new SoccerTeam[]{FCBayernMunich, Arsenal});
        match.setOfficiatedBy(referee);
        match.setPlayedAt(AllianzArena);
        System.out.println("New match: FC Bayern Munich vs Arsenal at Allianz Arena");
        
        //manage goals
        Goal goal1 = new Goal();
        goal1.setScoredBy(player1);
        goal1.setScoredIn(match);
        System.out.println("Player 1 scored a goal!");
        
        Goal goal2 = new Goal();
        goal2.setScoredBy(player2);
        goal2.setScoredIn(match);
        System.out.println("Player 2 scored a goal!");
        
        //create a season
        Season season2026 = new Season();
        season2026.getIncludes().add(match);
        System.out.println("Added match to 2026 season");
        
        //add season to league
        championsLeague.getOrganizes().add(season2026);
        
        //add teams to league
        championsLeague.getContains().add(FCBayernMunich);
        championsLeague.getContains().add(Arsenal);
        System.out.println("Added teams and season to Champions League");
        
        //add contracts

        Contract contract1 = new Contract();
        contract1.setBinds(player1);
        contract1.setWith(FCBayernMunich);
        System.out.println("Created contract between Player 1 and FC Bayern Munich");
        
        System.out.println("\nSummary of Champions League:");
        System.out.println("* Teams in league: " + championsLeague.getContains().size());
        System.out.println("* Seasons in league: " + championsLeague.getOrganizes().size());
        System.out.println("* Players in FC Bayern Munich: " + FCBayernMunich.getHas().size());

        
        System.out.println("* Teams in match: " + match.getInvolves().length);
        System.out.println("\nInheritance demo:");
        System.out.println("* Player is a Person: " + (player1 instanceof Person));
        System.out.println("* Coach is a Person: " + (coach instanceof Person));
        System.out.println("* Referee is a Person: " + (referee instanceof Person));
    }
}
