import collect_data
import make_html
import make_images



def main():
    print('------- Запущена загрузка и подготовка данных с сайта mlbb.io -------')
    collect_data.collect_data()
    print('\n\n')


    print("------- Запущено создание HTML файлов на основе данных ------")
    make_html.make_html()
    print('\n\n')


    print("------- Запущено создание изображений из HTML ------")
    make_images.make_images()
    print('\n\n')

    print("------- Изображения созданы и находятся в папаке final_images------")


if __name__ == "__main__":
    main()