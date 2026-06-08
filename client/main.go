package main

import (
	"context"
	"fmt"
	"log"
	"time"

	pb "golang_grpc_python_multi_function/pb"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func main() {

	conn, err := grpc.NewClient(
		"localhost:50051",
		grpc.WithTransportCredentials(
			insecure.NewCredentials(),
		),
	)

	if err != nil {
		log.Fatal(err)
	}

	defer conn.Close()

	client := pb.NewDemoServiceClient(conn)

	ctx, cancel := context.WithTimeout(
		context.Background(),
		5*time.Second,
	)

	defer cancel()

	addResp, err := client.Add(
		ctx,
		&pb.AddRequest{
			A: 10,
			B: 20,
		},
	)

	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Add Result:", addResp.Result)

	textResp, err := client.Uppercase(
		ctx,
		&pb.TextRequest{
			Text: "hello grpc",
		},
	)

	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Uppercase:", textResp.Result)
}
