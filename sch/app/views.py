from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
import os, requests, datetime
from random import randint
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}


def x_or_y_if_a(a, x, y):
    if a is None:
        return None
    elif not a:
        return x
    else:
        return y


def byte(a):
    return a * 8


def KB(a):
    return byte(a * 1024)


def MB(a):
    return KB(a * 1024)


def GB(a):
    return MB(a * 1024)


def TB(a):
    return GB(a * 1024)


def net_string(a):
    return a if a else 'нет'


def net_yest(a):
    return 'есть' if a else 'нет'


def net_da(a):
    return 'да' if a else "нет"


def human_read_format(size):
    l, k = ['бит', 'Б', 'КБ', 'МБ', 'ГБ', 'ТБ'], 0
    if size > 8:
        size /= 8
        k += 1
        print(size, k)
    while size >= 1024:
        k += 1
        size /= 1024
        print(size, k)
    return str(round(size)) + l[k]


def index(request):
    url_style = os.path.join('\static', 'css/style.css')
    data = {"style": url_style, "title": "Главная"}
    return render(request, 'app/index.html', context=data)


def product_list(request, product_type):
    d = []
    types = {'cpu': ('Процессоры', CPU),
             'gpu': ('Видеокарты', GPU),
             'motherboard': ('Материнские платы', Motherboard),
             'ram_dimm': ('Оперативная память DIMM', RAM_DIMM),
             'ram_so_dimm': ('Оперативная память SO-DIMM', RAM_SO_DIMM),
             'ssd': ('SSD', SSD),
             'hdd35': ('HDD 3.5', HDD35)}
    for item in types[product_type][1].objects.all():
        d.append({'title': item.title,
                  'price': item.price,
                  'rating': round(item.rating / max(1, item.rates), 1)})
        d[-1]["id"] = item.id
    style = os.path.join('\static', 'css/style.css')
    data_context = {"style": style,
                    "title": types[product_type][0],
                    "dictionary": d,
                    "type": product_type}
    return render(request, 'app/list.html', context=data_context)


def product(request, product_type, title):
    style = os.path.join('\static', 'css/style.css')
    tables = {'cpu': CPU, 'gpu': GPU, 'motherboard': Motherboard,
              'ram_dimm': RAM_DIMM, 'ram_so_dimm': RAM_SO_DIMM,
              'ssd': SSD, 'hdd35': HDD35}
    item = tables[product_type].objects.get(title=title)
    d = None
    if product_type == 'cpu':
        d = {
            'Гарантия': str(item.warranty) + ' мес.',
            'Страна выпуска': item.country,
            'Модель': item.title,
            'Поколение': item.generation,
            'Год выпуска': item.year,
            'Сокет': item.socket,
            'Система охлаждения': net_yest(item.has_cooling),
            'Термоинтерфейс': net_yest(item.term_interface),
            'Количество ядер': item.cores,
            'Максимальное количество потоков': item.threads,
            'Техпроцесс': str(item.tech_process) + ' нм',
            'Ядро': item.core,
            'Кэш L1 (инструкции)': human_read_format(item.cash_l1_instructions_bits),
            'Кэш L1 (данные)': human_read_format(item.cash_l1_data_bits),
            'Кэш L2': human_read_format(item.cash_l2_bits),
            'Кэш L3': human_read_format(item.cash_l3_bits),
            'Частота': str(item.base_freq) + ' ГГц',
            'Макс. частота': str(item.max_freq) + ' ГГц',
            'Свободный множитель': item.free_mult,
            'Тип памяти': item.memory,
            'Макс. объём памяти': human_read_format(item.max_mem_bits),
            'Каналы': item.channels,
            'минимальная частота ОЗУ': str(item.min_RAM_freq) + ' МГц',
            'максимальная частота ОЗУ': str(item.max_RAM_freq) + ' МГц',
            'ECC': net_yest(item.ECC),
            'TDP': str(item.TDP) + ' Вт',
            'Настраиваемая величина TDP': net_yest(item.custom_TDP),
            'Максимальная температура': str(item.max_temp) + '°',
            'Встроенное графическое ядро': net_yest(item.has_graphics),
            'PCI': item.PCI,
            'Число линий PCI Express': item.PCI_amount,
            'Пропускная способность шины': item.bandwidth,
            'Поддержка 64-битного набора команд': item.support_x64,
            'Многопоточность': net_yest(item.multi_thread),
            'Технология повышения частоты процессора': item.add_freq_tech,
            'Технология энергосбережения': item.energy_save_tech,
            # 'Описание': item.description,
            # 'Цена': item.price,
            # 'Оценка': round(item.rating / max(1, item.rates), 1),
            # 'rates': item.rates
        }
    elif product_type == 'gpu':
        d = {'Гарантия': str(item.warranty) + ' мес.',
             'Страна выпуска': item.country,
             'Название': item.title,
             'Год выпуска': item.year,
             'Код производителя': item.manufacturer_code,
             'Для майнинга': net_da(item.is_for_mining),
             'LHR': net_da(item.LHR),
             'Объём видеопамяти': human_read_format(item.memory),
             'Тип памяти': item.memory_type,
             'Пропускная способность памяти на один контакт': str(item.bandwidth) + ' Гбит/c',
             'Разрядность шины памяти': str(item.band_64x_32x) + ' бит',
             'Максимальная пропускная способность памяти': str(item.max_mem_bandwidth) + ' Гбайт/c',
             'Микроархитектура': item.micro_arc,
             'Кодовое название графического процессора ': item.graph_cpu,
             'Техпроцесс': str(item.techprocess) + 'нм',
             'Штатная частота работы видеочипа': str(item.chip_freq) + " МГц",
             'Количество универсальных процессоров (ALU)': item.ALU,
             'Число текстурных блоков': item.texture_blocks,
             'Число блоков растеризации ': item.raster_blocks,
             'Максимальная температура процессора': item.max_temp,
             'Поддержка трассировки лучей': net_yest(item.RTX),
             'Аппаратное ускорение трассировки лучей (RT-ядра)': net_yest(item.appart_accelerate_RT),
             'Тензорные ядра': item.tenz_cores,
             'Пиковая производительность чипов в FP32': str(item.max_efficiency_FP32) + ' GFLOPS',
             'Видеоразъемы': item.connectors,
             'Версия HDMI': item.HDMI_version,
             'Максимальное разрешение': item.max_resolution,
             'Количество подключаемых одновременно мониторов': item.max_monitors,
             'Интерфейс подключения': item.connection_interface,
             'Версия PCI Express': item.PCI_version,
             'Поддержка мультипроцессорной конфигурации': net_yest(item.support_mult_cpu_config),
             'Необходимость дополнительного питания': net_yest(item.need_extra_power),
             'Разъемы дополнительного питания': net_yest(item.extra_power_connections),
             'Максимальное энергопотребление': item.max_consuming_power,
             'Рекомендуемый блок питания': item.recommended_power,
             'Тип охлаждения': item.cooling,
             'Тип и количество установленных вентиляторов': item.type_and_amount_fans,
             'Управление скоростью вращения': net_yest(item.fan_speed_control),
             'Низкопрофильная карта (Low Profile)': net_da(item.low_profile),
             'Количество занимаемых слотов расширения': item.needed_slots,
             'Длина видеокарты': item.length,
             'Толщина видеокарты': item.width,
             'Вес': item.weight,
             'Подсветка элементов видеокарты': net_yest(item.illumination),
             'Синхронизация RGB подсветки': net_yest(item.synch_RGB),
             'LCD дисплей': net_yest(item.LCD),
             'Переключатель BIOS': net_yest(item.BIOS_switch),
             # 'Описание': item.description,
             # 'Цена': item.price,
             # 'Оценка': round(item.rating / max(1, item.rates), 1),
             # 'rates': item.rates,
        }
    elif product_type == 'motherboard':
        d = {'Гарантия': str(item.warranty) + ' мес.',
             'Страна выпуска': item.country,
             'Название': item.title,
             'Год выпуска': item.year,
             'Форм-фактор': item.form_factor,
             'Ширина': item.width,
             'Высота': item.height,
             'Сокет': item.socket,
             'Чипсет': item.chipset,
             'Встроенный центральный процессор': net_yest(item.built_in_cpu),
             'Модель встроенного центрального процессора': item.title_built_in_cpu,
             'Количество слотов памяти': item.memory_slots_amount,
             'Тип памяти': item.memory_type,
             'Частота оперативной памяти': item.ram_freq,
             'Максимальный объём памяти': human_read_format(item.max_memory),
             'Количество каналов памяти': item.memory_channels_amount,
             'Форм фактор поддерживаемой памяти': item.memory_form_factor,
             'Количество слотов M2': item.m2_slots_amount,
             'Количество слотов SATA': item.sata_slots_amount,
             'Поддержка NVMe': net_yest(item.nvme_support),
             'Режим работы SATA RAID': item.sata_raid_mode,
             'Разъёмы M2': net_string(item.m2_slots),
             'Форм-фактор M2': item.m2_form_factor,
             'Другие разъёмы накопителей': net_string(item.other_drive_slots),
             'Версия PCI Express': item.pci_express_version,
             'Количество слотов PCI-E x1': item.pci_e_x1_slots_amount,
             'Количество слотов PCI-E x16': item.pci_e_x16_slots_amount,
             'Поддержка SLI/CrossFire': net_yest(item.sli_crossfire_support),
             'Другие слоты расширения': item.other_expansion_slots,
             'Видеовыходы': item.video_outputs,
             'Количество и тип USB на задней панели': item.usb_amount_and_type,
             'Цифровые аудио порты (S/PDIF)': item.digital_and_audio_ports_s_pdif,
             'Другие разъемы на задней панели': item.other_slots_on_back_panel,
             'Количество сетевых портов (RJ-45)': item.network_ports_amount_rj45,
             '4-Pin PWM коннекторы для вентиляторов': item.fan_4pin_connectors,
             'Внутренние коннекторы USB на плате': item.internal_connectors_on_usb_plate_amount_and_type,
             'Разъем питания процессорного кулера': item.cpu_cooler_power_slot,
             'M.2 ключ E': net_yest(item.m2_e_key),
             'Интерфейс LPT': net_yest(item.lpt_interface),
             'Чипсет звукового адаптера': 'sound_adapter_chipset',
             'Звуковая схема': item.sound_scheme,
             'Встроенный адаптер Wi-Fi': item.built_in_wifi_adapter,
             'Bluetooth': net_string(item.bluetooth),
             'Скорость сетевого адаптера': item.network_adapter_speed,
             'Чипсет сетевого адаптера': item.network_adapter_chipset,
             'Количество фаз питания': item.power_phases_amount,
             'Разъем питания процессора': item.cpu_power_slot,
             'Пассивное охлаждение': item.passive_cooling,
             'Основной разъем питания': item.main_power_slot,
             'Подсветка элементов платы': net_yest(item.illumination),
             # 'Описание': item.description,
             # 'Цена': item.price,
             # 'Оценка': round(item.rating / max(1, item.rates), 1),
             # 'rates': item.rates,
        }
    elif product_type == 'ram_dimm':
        d = {'Гарантия': str(item.warranty) + ' мес.',
             'Страна выпуска': item.country,
             'Название': item.title,
             'Год выпуска': item.year,
             'Тип': item.common_type,
             'Тип памяти': item.type_ddr,
             'Ранговость': item.rang,
             'Регистровая память': net_da(item.register_memory),
             'ECC-память': net_yest(item.ecc_memory),
             'Память одного модуля': human_read_format(item.one_module_memory),
             'Суммарный объем памяти всего комплекта': human_read_format(GB(item.all_memory)),
             'Количество модулей в комплекте': item.modules_amount,
             'Тактовая частота': str(item.freq) + ' МГц',
             'CAS Latency (CL)': item.cas_latency_cl,
             'RAS to CAS Delay (tRCD)': item.ras_to_cas_delay_trcd,
             'Row Precharge Delay (tRP)': item.row_precharge_delay_trp,
             'Наличие радиатора': net_yest(item.has_radiator),
             'Высота': str(item.height) + ' мм',
             'Низкопрофильная (Low Profile)': net_da(item.low_profile),
             'Напряжение питания': str(item.power_voltage) + ' В',
             'Подсветка элементов платы': net_yest(item.illumination),
             'Цвет радиатора': item.radiator_color,
             # 'Описание': item.description,
             # 'Цена': item.price,
             # 'Оценка': round(item.rating / max(1, item.rates), 1),
             # 'rates': item.rates,
             }
    elif product_type == 'ram_so_dimm':
        d = {'Гарантия': str(item.warranty) + ' мес.',
             'Страна выпуска': item.country,
             'Название': item.title,
             'Тип': item.common_type,
             'Тип памяти': item.type_ddr,
             'Память одного модуля': human_read_format(item.one_module_memory),
             'Суммарный объем памяти всего комплекта': human_read_format(item.all_memory),
             'Количество модулей в комплекте': item.modules_amount,
             'Частота': str(item.freq) + ' МГц',
             'CAS Latency (CL)': item.cas_latency_cl,
             'RAS to CAS Delay (tRCD)': item.ras_to_cas_delay_trcd,
             'Row Precharge Delay (tRP)': item.row_precharge_delay_trp,
             'Количество чипов модуля': item.chips_amount,
             'Двухсторонняя установка чипов': net_yest(item.double_sided_chips_setup),
             'Напряжение питания': str(item.power_voltage) + ' В',
             # 'Описание': item.description,
             # 'Цена': item.price,
             # 'Оценка': round(item.rating / max(1, item.rates), 1),
             # 'rates': item.rates,
             }
    elif product_type == 'ssd':
        d = {
            'Гарантия': str(item.warranty) + ' мес.',
            'Название': item.title,
            'Тип': item.ssd_type,
            'Объём памяти (ГБ)': item.memory,
            'Физический интерфейс': item.phys_interface,
            'Количество бит на ячейку': item.bit_per_cell_amount,
            'Структура памяти': item.memory_structure,
            'DRAM буфер': net_yest(item.DRAM_buffer),
            'Максимальная скорость последовательного чтения': str(item.max_cons_reading_speed) + 'Мбайт/сек',
            'Максимальная скорость последовательной записи': str(item.max_cons_writing_speed) + 'Мбайт/сек',
            'Максимальный ресурс записи (TBW)': str(item.max_writing_resource_TBW) + 'ТБ',
            'DWPD': item.DWPD,
            'Аппаратное шифрование данных': net_yest(item.hardware_data_encryption),
            'Толщина (мм)': item.width,
            'Форм-фактор': x_or_y_if_a(item.form_factor, 'mSATA', '2.5"'),
            # 'Описание': item.description,
            # 'Цена': item.price,
            # 'Оценка': round(item.rating / max(1, item.rates), 1),
            # 'rates': item.rates,
        }
    elif product_type == 'hdd35':
        d = {
            'Гарантия': str(item.warranty) + ' мес.',
            'Название': item.title,
            'Объём памяти': human_read_format(item.memory_bits),
            'Скорость вращения': str(item.rotation_speed) + ' об/мин',
            'Объём кэш-памяти': human_read_format(item.cash_memory_bits),
            'Оптимизация под RAID-массивы': net_yest(item.raid_massives_optimization),
            'С гелиевым наполнением': net_yest(item.helium_fill),
            'Уровень шума во время работы': str(item.noise_dba) + ' дБа',
            'Технология записи': x_or_y_if_a(item.writing_tech_CMR_SMR, 'CMR', 'SMR'),
            'Число циклов позиционирования-парковки': item.position_park_cycles_amount,
            'Ширина': str(item.width) + ' мм',
            'Длина': str(item.length) + ' мм',
            'Высота': str(item.height) + ' мм',
            # 'Описание': item.description,
            # 'Цена': item.price,
            #' Оценка': round(item.rating / max(1, item.rates), 1),
            # 'rates': item.rates,
        }
    opinions_db = Opinion.objects.filter(pr_type=product_type, pr_title=title)
    opinions = []
    for i in opinions_db:
        user = User.objects.get(id=i.user_id)
        opinions.append([user.username, i.text, i.image])
    if not opinions:
        opinions = None
    data_context = {"style": style, "title": title, "item": d.items(), "product_type": product_type,
                    "opinions": opinions, "price": item.price, "description": item.description,
                    "rate": round(item.rating / max(1, item.rates), 1), "rates": item.rates}
    return render(request, 'app/product.html', context=data_context)


@login_required(login_url='/login')
def leave_rate(request, product_type, title, rate):
    types = {'cpu': CPU, 'gpu': GPU, 'motherboard': Motherboard,
             'ram_dimm': RAM_DIMM, 'ram_so_dimm': RAM_SO_DIMM,
             'ssd': SSD, 'hdd35': HDD35}
    table = types[product_type]
    item = table.objects.get(title=title)
    if item:
        item.rates += 1
        item.rating += int(rate)
        item.save(update_fields=['rates', 'rating'])
    else:
        print('no item')
    return HttpResponseRedirect(f'/product/{product_type}/{title}')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# def download_file(request, name):
#     if request.method == 'POST':
#         title = request.POST['title']
#         upload1 = request.FILES['upload']
#         object = Upload.objects.create(title=title, upload=upload1)
#         object.save()
#     return HttpResponseRedirect()


@login_required(login_url='/login')
def add_opinion(request, product_type, title):
    current_user = request.user
    if Opinion.objects.filter(pr_type=product_type,pr_title=title,user_id=current_user.id).exists():
        return HttpResponseRedirect('/product/' + product_type + '/' + title)
    style = os.path.join('\static', 'css/style.css')
    if request.method == 'POST':
        post = OpinionForm(request.POST, request.FILES)
        if post.is_valid():
            text, file = post.cleaned_data.get('text'), post.cleaned_data.get('file')
            op = Opinion()
            op.user_id = current_user.id
            op.text = text
            op.pr_type = product_type
            op.pr_title = title
            if file:
                op.image = file
            op.save()
            print('saved')
        return HttpResponseRedirect('/product/' + product_type + '/' + title)
    form_ = OpinionForm()
    data_context = {"style": style, "title": title, "product_type": product_type, "form": form_}
    return render(request, 'app/opinion.html', context=data_context)


@login_required(login_url='/login')
def profile(request):
    style = os.path.join('\static', 'css/style.css')
    data_context = {"style": style, "title": "Профиль"}
    return render(request, 'app/profile.html', context=data_context)


@login_required(login_url='/login')
def product_buy(request, product_type, title):
    tables = {'cpu': CPU, 'gpu': GPU, 'motherboard': Motherboard}
    item = tables[product_type].objects.get(title=title)
    price = item.price
    json_ = {
        "caption": "Покупка товара",
        "description": "Название: " + title,
        "meta": title + product_type + str(randint(100000, 999999)),
        "autoclear": True,
        "items": [
            {
                "name": title,
                "price": str(price),
                "nds": "nds_10",
                "currency": "RUB",
                "amount": 1,
                "image": {
                    "url": os.path.join('\static', f'img/{product_type}/{title}.jpg')
              }
            }
          ],
        "mode": "test",
        "return_url": "/product/" + product_type
        }
    requests.post('https://pay-sdk.yandex.net/v1', json=json_)
    return index(request)


def register(request):
    style = os.path.join('\static', 'css/style.css')
    if request.method == 'POST':
        post = DBLoginForm(request.POST)
        if post.is_valid():
            post.save()
            #post.clean()
            #username = post.cleaned_data.get('username')
            #surname = post.cleaned_data.get('surname')
            #name = post.cleaned_data.get('name')
            #email = post.cleaned_data.get('email')
            #hashed_password = post.cleaned_data.get('password')
            #user = User()
            #user.username = username
            #user.last_name = surname
            #user.first_name = name
            #user.email = email
            #user.date_joined = datetime.datetime.now()
            #user.last_login = user.date_joined
            #user.password = hashed_password
            #user.save()
            return HttpResponseRedirect('/')
        else:
            form = post
    else:
        form = DBLoginForm()
    data_context = {"style": style, "header": '<h2 style="color: white;">Регистрация</h2>', "title": "Авторизация",
                    "form": form}
    return render(request, 'app/sign_in.html', context=data_context)


def log_in(request):
    form = SignInForm()
    style = os.path.join('\static', 'css/style.css')
    if request.method == 'POST':
        post = SignInForm(request.POST)
        if post.is_valid():
            post.clean()
            email = post.cleaned_data.get('email')
            password = post.cleaned_data.get('password')
            remember_me = post.cleaned_data.get('remember_me')
            user = User.objects.get(email=email,password=password)# authenticate(request, email=password)
            if user:
                login(request, user)
                return HttpResponseRedirect("/")
        form = post
    data_context = {"title": "Авторизация", "form": form, "style": style}
    return render(request, 'app/login.html', context=data_context)


@login_required(login_url='/login')
def logout_(request):
    logout(request)