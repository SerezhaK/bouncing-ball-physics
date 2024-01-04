import matplotlib.pyplot as plt


def statistic(
        time_end=10,
        time_step=0.001,
        speed_angular_w=-10,
        speed_x_u=10,
        speed_y_v=3,
        radius=0.08,
        starting_coordinate_x=0,
        starting_coordinate_y=0,
        g=9.81
):
    # создаем массив значений времени
    time = []
    for i in range(0, int(time_end / time_step)):
        time.append(i)

    green_points = []
    red_points = []

    e_means = [0.1 * i for i in range(0, 11)]
    k_means = [0.1 * i for i in range(-10, 11)]

    for e in e_means:
        for k in k_means:
            coefficient_k = k
            coefficient_e = e
            ans = []

            # делаем копии исходных значений,
            # чтобы при новом проходе цикла не использовать старые
            new_coord_y = starting_coordinate_y
            new_coord_x = starting_coordinate_x
            speed_x_u_new = speed_x_u
            speed_y_v_new = speed_y_v
            speed_angular_w_new = speed_angular_w

            del_time = time[0]
            for i in time:
                delta_t = i - del_time
                del_time = i
                new_coord_x += speed_x_u_new * delta_t
                new_coord_y += speed_y_v_new * delta_t - (g * delta_t ** 2) / 2

                # speed_y_v_new += -0.001
                speed_y_v_new += -(g * delta_t)
                # При ударе считает два массива
                # согласно системе и решаем через систему уравнений
                if new_coord_y < 0:
                    # решение уравнений через новые переменные,
                    # чтобы в других уравнениях использовались старые значения
                    speed_x_u_ans = (2 / 7 * coefficient_k + 5 / 7) * speed_x_u_new + (
                            2 * k / 7 - 2 / 7) * radius * speed_angular_w_new
                    speed_y_v_ans = -1 * coefficient_e * speed_y_v_new
                    speed_angular_w_ans = (2 / 7 * coefficient_k - 5 / 7) * speed_x_u_new / radius + (
                            5 * k / 7 + 2 / 7) * speed_angular_w_new

                    # перезначения для активных переменных
                    speed_angular_w_new = speed_angular_w_ans
                    speed_y_v_new = speed_y_v_ans
                    speed_x_u_new = speed_x_u_ans

                    # для исключения проблем циклических ударов
                    new_coord_y = 0

                    # добавляем точку удара в массив
                    ans.append(new_coord_x)

                if len(ans) >= 2:
                    if ans[0] > ans[1] - ans[0]:
                        green_points.append([e, k])
                    else:
                        red_points.append([e, k])
                    break
                else:
                    time.append(time[-1] + delta_t)

    return green_points, red_points


# создание и настройка графика
fig, graph_axes = plt.subplots()

# добавление сетки и изменение делений осей
graph_axes.grid(True)
plt.yticks([0.1 * i for i in range(-10, 11)])
plt.xticks([0.1 * i for i in range(0, 11)])

# подписи осей
plt.xlabel("coefficient e")
plt.ylabel("coefficient k")

green_point, red_point = statistic()

for point in green_point:
    graph_axes.scatter(
        point[0], point[1], marker='o', linestyle='', color="green"
    )

for point in red_point:
    graph_axes.scatter(
        point[0], point[1], marker='o', linestyle='', color="red"
    )

plt.show()
