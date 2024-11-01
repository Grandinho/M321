// main.go
package main

import (
    "context"
    "fmt"
    "log"
    "os"
    "time"

    pb "your-module/api/unsafe/sensor_void_energy"
    "google.golang.org/grpc"
)

func main() {
    // GRPC Server Adresse aus Umgebungsvariablen
    serverAddr := fmt.Sprintf("%s:%s",
        os.Getenv("GRPC_SERVER_HOST"),
        os.Getenv("GRPC_SERVER_PORT"))

    // Verbindung zum GRPC Server aufbauen
    conn, err := grpc.Dial(serverAddr, grpc.WithInsecure())
    if err != nil {
        log.Fatalf("Failed to connect: %v", err)
    }
    defer conn.Close()

    // GRPC Client erstellen
    client := pb.NewSensorVoidEnergyServerClient(conn)

    // Kontinuierlich Sensordaten abrufen
    for {
        // GRPC Aufruf
        response, err := client.ReadSensorData(context.Background(), &pb.Void{})
        if err != nil {
            log.Printf("Error reading sensor data: %v", err)
            time.Sleep(5 * time.Second)
            continue
        }

        // Verarbeite die Sensordaten
        processSensorData(response.Hexdata)

        // Kurze Pause zwischen den Abfragen
        time.Sleep(1 * time.Second)
    }
}

func processSensorData(hexdata string) {
    // Hier kommt deine Logik zur Verarbeitung der Sensordaten hin
    log.Printf("Received sensor data: %s", hexdata)
}