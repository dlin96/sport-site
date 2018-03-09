import depth_chart

if __name__ == '__main__':
    depth_chart.populate()
    while True:
        user_in = input("Enter a team name: ").lower()
        depth_chart.main(user_in)
        bool_cont = input("Another team? ")
        if bool_cont == 'no':
            break