import random,math,copy

width_cell_count = 28
height_cell_count = 28
e = math.e
learn_rate = 0.4
layers_count = 4
layers_layer_count = [width_cell_count*height_cell_count,16,16,10]
layers = []
for i in layers_layer_count:
    l = []
    for x in range(i):
        l.append(0)
    layers.append(l)

def random_weights():
    global W
    W = []
    for i in range(layers_count-1):
        w = []
        for m in range(layers_layer_count[i+1]):
            M = []
            for n in range(layers_layer_count[i]+1):
                M.append(random.randint(-100,100)/100)
            w.append(M)
        W.append(w)

def sigmoid(x):
    if x < -30:
        return 10**(-20)
    elif x > 30:
        return 1-10**(-20)
    return 1 / (1 + math.exp(-x))

def process():
    layers[0] = []
    for y in map_cell:
        for x in y:
            layers[0].append(x)

    for i in range(layers_count-1):
        for x in range(layers_layer_count[i+1]):
            a = 0
            for c in range(layers_layer_count[i]):
                a += W[i][x][c]*layers[i][c]
            a += W[i][x][-1]
            layers[i+1][x] = sigmoid(a)

def clear():
    global map_cell
    map_cell=[]
    for y in range(height_cell_count):
        m = []
        for x in range(width_cell_count):
            m.append(0)
        map_cell.append(m)

def number_max():
    o = max(layers[-1])
    for i in range(len(layers[-1])):
        if o == layers[-1][i]:
            o = i
            break
    return o

def back_propagation(target,w_dif = [],koef = 1):
    if w_dif == []:
        for i in range(layers_count-1):
            w = []
            for _ in range(layers_layer_count[i+1]):
                m = []
                for _ in range(layers_layer_count[i]+1):
                    m.append(0)
                w.append(m)
            w_dif.append(w)
    for i in range(layers_count-1):
        n_C = []
        for _ in range(layers_layer_count[-1-i]):
            n_C.append(0)
        if i == 0:
            for j in range(layers_layer_count[-1]):
                n_C[j] = layers[-1][j] * (1-layers[-1][j]) * (layers[-1][j]-target[j])
        else:
            for k in range(layers_layer_count[-1-i]):
                for j in range(layers_layer_count[-i]):
                    n_C[k] += W[-i-1][j][k] * C[j]
                n_C[k] *= layers[-1-i][k] * (1-layers[-1-i][k])
        
        C = copy.deepcopy(n_C)
        for j in range(layers_layer_count[-1-i]):
            for k in range(layers_layer_count[-2-i]):
                w_dif[-1-i][j][k] -= learn_rate * C[j] * layers[-2-i][k]
                w_dif[-1-i][j][k] *= koef
            w_dif[-1-i][j][-1] -= learn_rate * C[j]
            w_dif[-1-i][j][-1] *= koef
    return w_dif

def weight_change(W,w_dif):
    for i in range(layers_count-1):
        for j in range(layers_layer_count[-1-i]):
            for k in range(layers_layer_count[-2-i]):
                W[-1-i][j][k] += w_dif[-1-i][j][k]
    return W

random_weights()
clear()
process()

print('0 - С демострацией')
print('1 - Только обучение')
print('2 - Проверка правильности алгоритма')
a = input()
if a == '0':
    import pygame
    import linecache
    
    with open('w.txt', 'r') as f:
        W = []
        for i in range(layers_count-1):
            w = []
            for m in range(layers_layer_count[i+1]):
                w.append(list(map(float,f.readline().split())))
            W.append(w)
        for i,line in enumerate(f):
            print(i,line)
    f.close()
    
    pygame.init()
    width = 1600
    height = 900
    t = 0.75    # Значение для изменения размера окна
    win=pygame.display.set_mode((width * t,height * t)) # Создание окна программы
    pygame.display.set_caption("Распознавание")

    width_cell = height / width_cell_count
    height_cell = height / height_cell_count

    fonts =[]
    for i in range(1,201):
        fonts.append(pygame.font.SysFont("microsofttai le",i))

    clock=pygame.time.Clock()

    click_d=0
    color = 1
    clear_button = 0
    web_button = 1

    run=True
    while run:
        delta = clock.tick()
        win.fill((0,0,0))

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            elif event.type == pygame.MOUSEBUTTONDOWN: #Фиксация нажатия клавиши мыши
                click_d=1
            elif event.type == pygame.MOUSEBUTTONUP:
                click_d=0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c: # Очистка поля по нажатию 'c'
                    clear()
                elif event.key == pygame.K_1: #
                    color=0                   # Выбор цвета закрашивания
                elif event.key == pygame.K_2: # клавиша '1' - чёрный
                    color=1                   # клавиша '2' - белый

        if click_d:
            for x in range(width_cell_count):
                for y in range(height_cell_count):                                                                             #Закрашивание поля
                    if x*width_cell<=event.pos[0] / t<(x+1)*width_cell and y*height_cell<=event.pos[1] / t<(y+1)*height_cell:
                        map_cell[y][x]=color
                        process()
                        break
            else:
                for i in range(10):
                    if height+60+i*60<=event.pos[0] / t<height+60+i*60+40 and 20<=event.pos[1] / t<60:
                        print(i)
                        click_d = 0
                        cost_mistake = 0
                        for a in range(10):
                            cost_mistake += (layers[-1][a]-int(a==i))**2
                        print(cost_mistake)
                        process()
                        if clear_button:
                            clear()
                        break
                else:
                    if height+60<=event.pos[0] / t<height+100 and 100<=event.pos[1] / t<140:
                        clear_button = 1-clear_button
                        click_d = 0
                    elif height+120<=event.pos[0] / t<height+160 and 100<=event.pos[1] / t<140:
                        web_button = 1-web_button
                        click_d = 0

        # Отрисовка сетки
        for x in range(width_cell_count):                                                                                         #Отображение
            for y in range(height_cell_count):                                                                                    #поля
                pygame.draw.rect(win,(255*map_cell[y][x],)*3,(width_cell*x * t,height_cell*y * t,width_cell * t,height_cell * t)) #
        for i in range(height_cell_count+1):                                                                                      #
            pygame.draw.line(win,(200,200,200),(0,height_cell*i * t),(height * t,height_cell*i * t),1)                            #
        for i in range(width_cell_count+1):                                                                                       #
            pygame.draw.line(win,(200,200,200),(width_cell*i * t,0),(width_cell*i * t,height * t),1)                              #
        # Отрисовка кнопок с цифрами и ответ нейросети
        for i in range(10):
            pygame.draw.rect(win,(200,)*3,((height+59+i*60) * t,19 * t,43 * t,43 * t))
            pygame.draw.rect(win,(255*layers[-1][i],)*3,((height+60+i*60) * t,20 * t,40 * t,40 * t))
            win.blit(fonts[19].render(str(i),1,(255,255,255)),((height+75+i*60) * t,65 * t))
        o = number_max()
        win.blit(fonts[int(80 * t)].render(str(o),1,(255,255,255)),((height+600) * t,90 * t))
        pygame.draw.rect(win,(200,)*3,((height+59) * t,99 * t,43 * t,43 * t))
        pygame.draw.rect(win,(255*clear_button,)*3,((height+60) * t,100 * t,40 * t,40 * t))
        # Отрисовка нейронов и весов
        pygame.draw.rect(win,(200,)*3,((height+119) * t,99 * t,43 * t,43 * t))
        pygame.draw.rect(win,(255*web_button,)*3,((height+120) * t,100 * t,40 * t,40 * t))
        if web_button:
            for i in range(len(layers)-1):
                if layers_layer_count[i]>20:
                    l_1=layers[i][:10]+layers[i][-10:]
                else:
                    l_1=layers[i]
                if layers_layer_count[i+1]>20:
                    l_2=layers[i+1][:10]+layers[i+1][-10:]
                else:
                    l_2=layers[i+1]
                for a in range(len(l_1)):
                    for b in range(len(l_2)):
                        pygame.draw.line(win,    (max(min(100,100/10*W[i][b][a]),min(255,255/10*(-W[i][b][a]))), max(min(120,120/10*(-W[i][b][a])),min(200,200/10*W[i][b][a])),
                                                  max(min(120,120/10*(-W[i][b][a])),min(255,255/10*W[i][b][a]))),
                                         ((height+50+200*i) * t,(450+(a-len(l_1)/2)*25) * t),((height+50+200*(i+1)) * t,(450+(b-len(l_2)/2)*25) * t),1)
                    pygame.draw.circle(win,(200,)*3,((height+50+200*i) * t,(450+(a-len(l_1)/2)*25) * t),12.1 * t)
                    pygame.draw.circle(win,(255*l_1[a],)*3,((height+50+200*i) * t,(450+(a-len(l_1)/2)*25) * t),10 * t)
            for a in range(layers_layer_count[-1]):
                pygame.draw.rect(win,(200,)*3,((height+39+(i+1)*200) * t,(450-11+(a-len(layers[-1])/2)*25) * t,23 * t,23 * t))
                pygame.draw.rect(win,(255*layers[-1][a],)*3,((height+40+(i+1)*200) * t,(450-10+(a-len(layers[-1])/2)*25) * t,20 * t,20 * t))
                win.blit(fonts[int(10 * t)].render(str(a),1,(255,255,255)),((height+65+(i+1)*200) * t,(450-7+(a-len(layers[-1])/2)*25) * t))
            for i in range(layers_layer_count[1]):
                pygame.draw.rect(win,(200,)*3,((height+39+(i%(layers_layer_count[1]//2))*80) * t,(729+(i//(layers_layer_count[1]//2))*80) * t,(width_cell_count*2+2),(height_cell_count*2+2)))
                for y in range(height_cell_count):
                    for x in range(width_cell_count):
                        pygame.draw.rect(win,    (max(min(100,100/10*W[0][i][y*width_cell_count+x]),min(255,255/10*(-W[0][i][y*width_cell_count+x]))),
                                                  max(min(120,120/10*(-W[0][i][y*width_cell_count+x])),min(200,200/10*W[0][i][y*width_cell_count+x])),
                                                  max(min(120,120/10*(-W[0][i][y*width_cell_count+x])),min(255,255/10*W[0][i][y*width_cell_count+x]))),
                                         ((height+40+(i%(layers_layer_count[1]//2))*80) * t +x*2,(730+(i//(layers_layer_count[1]//2))*80) * t +y*2,2,2))


        pygame.display.update()

    pygame.quit()
elif a in ['1','2']:
    from keras.datasets import mnist
    import os
    
    (x_train, y_train), (x_test, y_test) = mnist.load_data(path = os.getcwd()+'\dataset\mnist.npz')
    if a == '1':
        for b in range(600):
            w_dif = []
            for k in range(100):
                i = k + b * 100
                map_cell = []
                for x in x_train[i]:
                    m = []
                    for n in x:
                        m.append((n/255))
                    map_cell.append(m)
                process()
                target = []
                for _ in range(10):
                    target.append(0.2)
                target[y_train[i]] = 1
                if k == 99:
                    break
                back_propagation(target,w_dif)
            back_propagation(target,w_dif,0.01)
            W = weight_change(W,w_dif)
            print(b)

        with open('w.txt', 'w') as f:
            for i in W:
                for j in i:
                    f.write(' '.join(map(str,j))+'\n')
        f.close()
    elif a == '2':
        import linecache
    
        with open('w.txt', 'r') as f:
            W = []
            for i in range(layers_count-1):
                w = []
                for m in range(layers_layer_count[i+1]):
                    w.append(list(map(float,f.readline().split())))
                W.append(w)
            for i,line in enumerate(f):
                print(i,line)
        f.close()
        
        t = 0
        for i in range(10000):
            map_cell = []
            for x in x_test[i]:
                m = []
                for n in x:
                    m.append(math.ceil(n/255))
                map_cell.append(m)
            process()
            o = number_max()
            t += int(o == y_test[i])
            if i % 1000 == 999:
                print(i//1000)
        print(str(round(t/10000*100,3))+'%')
