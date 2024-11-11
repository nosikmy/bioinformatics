from redun import task, Scheduler

redun_namespace = "hello_world"

@task()
def get_planet():
    return "World"

@task()
def greeter(greet: str, thing: str):
    return "{}, {}!".format(greet, thing)

@task()
def main(greet: str="Hello"):
    return greeter(greet, get_planet())

if __name__ == "__main__":
    scheduler = Scheduler()
    result = scheduler.run(main())
    print(result)
