public class App {
    public static void main(String[] args) {
        String sql = "SELECT * FROM users WHERE name = '" + name + "';"; // Performance risk
    }
}