import java.sql.*;
import java.util.*;

public class HotelApp {
    public static void main(String[] args) {
        createTables();
    }

    public static void createTables() {
        Connection conn = null;
        try {
            Class.forName("org.sqlite.JDBC");
            conn = DriverManager.getConnection("jdbc:sqlite:hotel.db");
            Statement stmt = conn.createStatement();

            String sql = "CREATE TABLE IF NOT EXISTS rooms (" +
                    "room_number INTEGER PRIMARY KEY," +
                    "room_type TEXT," +
                    "is_available INTEGER)";
            stmt.execute(sql);

            sql = "CREATE TABLE IF NOT EXISTS bookings (" +
                    "booking_id INTEGER PRIMARY KEY," +
                    "room_number INTEGER," +
                    "guest_name TEXT," +
                    "check_in DATE," +
                    "check_out DATE," +
                    "FOREIGN KEY (room_number) REFERENCES rooms (room_number))";
            stmt.execute(sql);

            conn.close();
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    public static void bookRoom(String roomType, String checkIn, String checkOut, String guestName) {
        Connection conn = null;
        try {
            Class.forName("org.sqlite.JDBC");
            conn = DriverManager.getConnection("jdbc:sqlite:hotel.db");
            PreparedStatement pstmt = conn.prepareStatement("SELECT * FROM rooms WHERE room_type = ? AND is_available = 1");
            pstmt.setString(1, roomType);
            ResultSet row = pstmt.executeQuery();

            if (row.next()) {
                pstmt = conn.prepareStatement("INSERT INTO bookings (room_number, guest_name, check_in, check_out) VALUES (?, ?, ?, ?)");
                pstmt.setInt(1, row.getInt("room_number"));
                pstmt.setString(2, guestName);
                pstmt.setString(3, checkIn);
                pstmt.setString(4, checkOut);
                pstmt.executeUpdate();

                pstmt = conn.prepareStatement("UPDATE rooms SET is_available = 0 WHERE room_number = ?");
                pstmt.setInt(1, row.getInt("room_number"));
                pstmt.executeUpdate();

                conn.close();
                System.out.println("Room booked successfully");
            } else {
                conn.close();
                System.out.println("No available rooms of this type");
            }
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    public static void checkAvailability(String roomType, String checkIn, String checkOut) {
        Connection conn = null;
        try {
            Class.forName("org.sqlite.JDBC");
            conn = DriverManager.getConnection("jdbc:sqlite:hotel.db");
            PreparedStatement pstmt = conn.prepareStatement("SELECT * FROM rooms WHERE room_type = ? AND is_available = 1");
            pstmt.setString(1, roomType);
            ResultSet rows = pstmt.executeQuery();

            int count = 0;
            while (rows.next()) {
                count++;
            }

            if (count > 0) {
                System.out.println("Available rooms: " + count);
            } else {
                System.out.println("No available rooms of this type");
            }

            conn.close();
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    public static void manageRooms(String roomNumber, String roomType, String action) {
        Connection conn = null;
        try {
            Class.forName("org.sqlite.JDBC");
            conn = DriverManager.getConnection("jdbc:sqlite:hotel.db");
            PreparedStatement pstmt = null;

            if (action.equals("add")) {
                pstmt = conn.prepareStatement("INSERT INTO rooms (room_number, room_type, is_available) VALUES (?, ?, 1)");
                pstmt.setString(1, roomNumber);
                pstmt.setString(2, roomType);
            } else if (action.equals("delete")) {
                pstmt = conn.prepareStatement("DELETE FROM rooms WHERE room_number = ?");
                pstmt.setString(1, roomNumber);
            } else if (action.equals("update")) {
                pstmt = conn.prepareStatement("UPDATE rooms SET room_type = ? WHERE room_number = ?");
                pstmt.setString(1, roomType);
                pstmt.setString(2, roomNumber);
            }

            pstmt.executeUpdate();

            conn.close();
            System.out.println("Room " + action + "ed successfully");
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }
}