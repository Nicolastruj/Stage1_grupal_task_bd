import crawler_controller
import time

def main():
    interval = 20
    path = "./Datamart_libros"

    crawler_controller.periodic_task(interval, path)

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()












