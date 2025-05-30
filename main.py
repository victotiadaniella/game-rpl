import pygame
import sys
import time
import random

# Inisialisasi Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Animasi Gerak Karakter dengan Rumah")
clock = pygame.time.Clock()

# Load frame animasi untuk setiap arah (2 frame jalan)
walk_up_frames = [
    pygame.image.load("character_gerak/up3.png").convert_alpha(),
    pygame.image.load("character_gerak/up4.png").convert_alpha()
]

walk_down_frames = [
    pygame.image.load("character_gerak/down3.png").convert_alpha(),
    pygame.image.load("character_gerak/down4.png").convert_alpha()
]

walk_left_frames = [
    pygame.image.load("character_gerak/left2.png").convert_alpha(),
    pygame.image.load("character_gerak/left4.png").convert_alpha()
]

walk_right_frames = [
    pygame.image.load("character_gerak/right3.png").convert_alpha(),
    pygame.image.load("character_gerak/right4.png").convert_alpha()
]

# Frame idle untuk tiap arah (2 frame animasi idle per arah)
idle_frames = {
    "up": [
        pygame.image.load("character_diam/idle_up.png").convert_alpha(),
        pygame.image.load("character_diam/idle_up1.png").convert_alpha()
    ],
    "down": [
        pygame.image.load("character_diam/idle_down1.png").convert_alpha(),
        pygame.image.load("character_diam/idle_down2.png").convert_alpha()
    ],
    "left": [
        pygame.image.load("character_diam/idle_left.png").convert_alpha(),
        pygame.image.load("character_diam/idle_left1.png").convert_alpha()
    ],
    "right": [
        pygame.image.load("character_diam/idle_right.png").convert_alpha(),
        pygame.image.load("character_diam/idle_right1.png").convert_alpha()
    ]
}

# Sprite saat karakter menggunakan alat
tool_sprites = {
    "up": [
        pygame.image.load("character_penyiram/up.png").convert_alpha(),
        pygame.image.load("character_penyiram/up2.png").convert_alpha()
    ],
    "down": [
        pygame.image.load("character_penyiram/down.png").convert_alpha(),
        pygame.image.load("character_penyiram/down1.png").convert_alpha()
    ],
    "left": [
        pygame.image.load("character_penyiram/left.png").convert_alpha(),
        pygame.image.load("character_penyiram/left0.png").convert_alpha()
    ],
    "right": [
        pygame.image.load("character_penyiram/right.png").convert_alpha(),
        pygame.image.load("character_penyiram/right1.png").convert_alpha()
    ]
}

# Fungsi untuk memuat gambar dengan aman
def safe_load_image(path, scale_size=None):
    try:
        img = pygame.image.load(path).convert_alpha()
        if scale_size:
            img = pygame.transform.scale(img, scale_size)
        return img
    except Exception as e:
        print(f"Gagal memuat {path}: {e}")
        return None

def scale_image(img, scale_factor):
    if img is None:
        return None
    w, h = img.get_size()
    return pygame.transform.scale(img, (int(w * scale_factor), int(h * scale_factor)))

SCALE = 2  # Faktor pembesaran

# Load sprites dengan error handling
house_sprite = safe_load_image("alat/rumah.png", (100, 80))
if house_sprite:
    house_sprite = scale_image(house_sprite, SCALE)

bed_img = safe_load_image("alat/bed.png")
table_img = safe_load_image("alat/meja.png") 
chair_img = safe_load_image("alat/kursi.png")
sofa_img = safe_load_image("alat/laci.png")
tree_img = safe_load_image("alat/pohon.png", (96, 128))
stump_img = safe_load_image("alat/batang_pohon.png", (48, 32))
bush_img = safe_load_image("alat/semak-semak_berbuah.png", (64, 48))
fruit_sprite = safe_load_image("alat/buah.png")

# Skala frame karakter
walk_up_frames = [scale_image(img, SCALE) for img in walk_up_frames]
walk_down_frames = [scale_image(img, SCALE) for img in walk_down_frames]
walk_left_frames = [scale_image(img, SCALE) for img in walk_left_frames]
walk_right_frames = [scale_image(img, SCALE) for img in walk_right_frames]

idle_frames = {
    key: [scale_image(frame, SCALE) for frame in frames]
    for key, frames in idle_frames.items()
}

tool_sprites = {
    key: [scale_image(frame, SCALE) for frame in frames]
    for key, frames in tool_sprites.items()
}

# Skala furnitur
if bed_img: bed_img = scale_image(bed_img, SCALE)
if table_img: table_img = scale_image(table_img, SCALE)
if chair_img: chair_img = scale_image(chair_img, SCALE)
if sofa_img: sofa_img = scale_image(sofa_img, SCALE)

inventory = ["cangkul"]
selected_index = 0

# Fungsi untuk menambah item ke inventory
def add_to_inventory(item):
    """Tambahkan item ke inventory"""
    inventory.append(item)
    print(f"{item} ditambahkan ke inventory!")

# Fungsi untuk menghitung jumlah item tertentu di inventory
def count_item_in_inventory(item):
    """Hitung jumlah item tertentu di inventory"""
    return inventory.count(item)

# Icon alat
tool_icons = {
    "cangkul": safe_load_image("alat/alat_penyiram.png"),
    "buah": safe_load_image("alat/buah.png")  # Icon untuk buah di inventory
}

# Skala icon inventory
if tool_icons["cangkul"]:
    tool_icons["cangkul"] = scale_image(tool_icons["cangkul"], 1.5)
if tool_icons["buah"]:
    tool_icons["buah"] = scale_image(tool_icons["buah"], 1.5)

# Posisi furniture luar rumah
outdoor_furniture = {
    "tree": [(150, 300), (600, 250)],
    "stump": [(500, 400)],
    "bush": [(200, 500), (550, 350)]
}

# Koordinat furnitur dalam rumah
furniture_positions = {
    "bed": (250, 250),
    "table": (130, 130),
    "chair": (105, 125),
    "sofa": (220, 220)
}

# Latar dalam rumah
interior_bg = pygame.Surface((400, 300))
interior_bg.fill((245, 222, 179))  # Light brown

# Class untuk pohon buah yang diperbaiki
class Tree:
    def __init__(self, pos, growth_time, fruit_sprite):
        self.pos = pos
        self.growth_time = growth_time  # dalam detik
        self.plant_time = time.time()
        self.fruit_sprite = fruit_sprite
        self.has_fruit = False
        # List untuk menyimpan buah yang tersedia (True = ada buah, False = sudah dipanen)
        self.fruit_positions = []
        self.available_fruits = []

    def _generate_fruit_positions(self):
        """Generate posisi buah yang realistis dalam area dedaunan pohon"""
        positions = []
        available = []
        if tree_img:
            tree_width = tree_img.get_width()
            tree_height = tree_img.get_height()
            
            # Area dedaunan pohon (bagian atas 60% dari pohon)
            canopy_start_y = int(tree_height * 0.2)  # Mulai dari 20% dari atas pohon
            canopy_end_y = int(tree_height * 0.7)    # Sampai 70% dari atas pohon
            canopy_width = int(tree_width * 0.8)     # 80% dari lebar pohon
            canopy_offset_x = int(tree_width * 0.1)  # Offset 10% dari kiri
            
            # Generate 3-5 buah per pohon dengan posisi random
            num_fruits = random.randint(3, 5)
            for _ in range(num_fruits):
                # Posisi X dalam area dedaunan
                fruit_x = random.randint(canopy_offset_x, canopy_offset_x + canopy_width - 16)
                # Posisi Y dalam area dedaunan
                fruit_y = random.randint(canopy_start_y, canopy_end_y)
                
                # Tambahkan sedikit variasi untuk terlihat lebih natural
                fruit_x += random.randint(-8, 8)
                fruit_y += random.randint(-8, 8)
                
                positions.append((fruit_x, fruit_y))
                available.append(True)  # Semua buah tersedia saat pertama kali tumbuh
        
        self.fruit_positions = positions
        self.available_fruits = available

    def update(self):
        current_time = time.time()
        if not self.has_fruit and current_time - self.plant_time >= self.growth_time:
            self.has_fruit = True
            self._generate_fruit_positions()

    def draw(self, surface, tree_sprite):
        # Gambar pohon terlebih dahulu
        if tree_sprite:
            surface.blit(tree_sprite, self.pos)
            
        # Gambar buah-buah yang masih tersedia
        if self.has_fruit and self.fruit_sprite:
            for i, (fruit_pos, available) in enumerate(zip(self.fruit_positions, self.available_fruits)):
                if available:  # Hanya gambar buah yang masih tersedia
                    # Hitung posisi absolut buah berdasarkan posisi pohon
                    absolute_fruit_x = self.pos[0] + fruit_pos[0]
                    absolute_fruit_y = self.pos[1] + fruit_pos[1]
                    
                    # Pastikan buah tidak keluar dari batas layar
                    if (0 <= absolute_fruit_x <= 800 - self.fruit_sprite.get_width() and 
                        0 <= absolute_fruit_y <= 600 - self.fruit_sprite.get_height()):
                        surface.blit(self.fruit_sprite, (absolute_fruit_x, absolute_fruit_y))

    def harvest_single_fruit(self, player_pos):
        """Panen satu buah terdekat dengan player"""
        if not self.has_fruit:
            return False
            
        closest_fruit_index = -1
        closest_distance = float('inf')
        
        # Cari buah terdekat yang masih tersedia
        for i, (fruit_pos, available) in enumerate(zip(self.fruit_positions, self.available_fruits)):
            if available:
                # Posisi absolut buah
                absolute_fruit_x = self.pos[0] + fruit_pos[0]
                absolute_fruit_y = self.pos[1] + fruit_pos[1]
                
                # Hitung jarak ke player
                distance = ((player_pos[0] - absolute_fruit_x) ** 2 + 
                           (player_pos[1] - absolute_fruit_y) ** 2) ** 0.5
                
                if distance < closest_distance:
                    closest_distance = distance
                    closest_fruit_index = i
        
        # Panen buah terdekat jika ada
        if closest_fruit_index >= 0:
            self.available_fruits[closest_fruit_index] = False
            
            # Cek apakah masih ada buah tersisa
            if not any(self.available_fruits):
                # Jika semua buah sudah dipanen, reset pohon untuk tumbuh lagi
                self.has_fruit = False
                self.plant_time = time.time()
                self.fruit_positions = []
                self.available_fruits = []
            
            return True
        
        return False

    def has_available_fruits(self):
        """Cek apakah masih ada buah yang bisa dipanen"""
        return self.has_fruit and any(self.available_fruits)

    def is_near(self, player_pos, distance=80):
        if tree_img:
            tree_rect = pygame.Rect(self.pos[0], self.pos[1], tree_img.get_width(), tree_img.get_height())
        else:
            tree_rect = pygame.Rect(self.pos[0], self.pos[1], 96, 128)
        player_rect = pygame.Rect(player_pos[0], player_pos[1], 64, 64)
        return tree_rect.colliderect(player_rect.inflate(distance, distance))

# Fungsi UI dan collision
def draw_inventory():
    slot_width = 40
    slot_height = 40
    spacing = 10
    start_x = 10
    start_y = 10
    
    # Hitung item unik dan jumlahnya
    unique_items = {}
    for item in inventory:
        unique_items[item] = unique_items.get(item, 0) + 1
    
    # Gambar slot inventory untuk item unik
    for i, (item, count) in enumerate(unique_items.items()):
        x = start_x + i * (slot_width + spacing)
        color = (255, 255, 255) if i == selected_index else (150, 150, 150)
        pygame.draw.rect(screen, color, (x, start_y, slot_width, slot_height), 2)
        
        # Gambar icon item
        if item in tool_icons and tool_icons[item]:
            icon = pygame.transform.scale(tool_icons[item], (32, 32))
            screen.blit(icon, (x + 4, start_y + 4))
        
        # Gambar jumlah item jika lebih dari 1
        if count > 1:
            font = pygame.font.Font(None, 16)
            count_text = font.render(str(count), True, (255, 255, 0))
            screen.blit(count_text, (x + slot_width - 15, start_y + slot_height - 15))

def draw_instructions():
    font = pygame.font.Font(None, 24)
    instructions = [
        "WASD: Gerak",
        "E: Ambil alat",
        "Q: Simpan alat", 
        "SPACE: Gunakan alat",
        "F: Masuk/Keluar rumah",
        "ENTER: Panen buah"
    ]
    for i, instruction in enumerate(instructions):
        text = font.render(instruction, True, (255, 255, 255))
        screen.blit(text, (10, 70 + i * 25))

def check_house_collision(player_x, player_y, player_width=64, player_height=64):
    if not house_sprite:
        return False
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    house_rect = pygame.Rect(house_x + 50, house_y + 120, 100, 40)
    return player_rect.colliderect(house_rect)

# Variabel game
frame_index = 0
direction = "down"
animation_timer = 0
walk_animation_speed = 200
idle_animation_speed = 333
x, y = 300.0, 400.0
speed = 0.15

# Variabel rumah
house_x = 400
house_y = 200
inside_house = False

# Variabel alat
has_tool = False
using_tool = False

# Buat pohon buah dengan posisi yang lebih tersebar (30 detik untuk testing)
trees = [
    Tree(pos=(150, 300), growth_time=30, fruit_sprite=fruit_sprite),
    Tree(pos=(600, 250), growth_time=30, fruit_sprite=fruit_sprite),
    Tree(pos=(350, 450), growth_time=30, fruit_sprite=fruit_sprite),
    Tree(pos=(80, 180), growth_time=30, fruit_sprite=fruit_sprite)
]

running = True

# Game loop utama
while running:
    dt = clock.tick(60)
    animation_timer += dt

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                has_tool = True
                selected_index = (selected_index + 1) % len(inventory)
            elif event.key == pygame.K_q:
                has_tool = False
                using_tool = False
                selected_index = (selected_index - 1) % len(inventory)
            elif event.key == pygame.K_SPACE and has_tool:
                using_tool = True
            elif event.key == pygame.K_f:
                if not inside_house and check_house_collision(x, y):
                    inside_house = True
                    x, y = 100.0, 200.0  # Posisi spawn dalam rumah
                elif inside_house:
                    inside_house = False
                    x, y = house_x + 100, house_y + 170  # Posisi keluar rumah
            elif event.key == pygame.K_RETURN:
                # Panen buah satu per satu dari pohon terdekat
                for tree in trees:
                    if tree.is_near((x, y)) and tree.has_available_fruits():
                        if tree.harvest_single_fruit((x, y)):
                            add_to_inventory("buah")
                            fruit_count = count_item_in_inventory("buah")
                            print(f"Satu buah dipanen! Total buah: {fruit_count}")
                            break
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                using_tool = False

    # Input gerakan
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    moved = False

    if keys[pygame.K_w]:
        dy = -1
        direction = "up"
        moved = True
    elif keys[pygame.K_s]:
        dy = 1
        direction = "down"
        moved = True
    elif keys[pygame.K_a]:
        dx = -1
        direction = "left"
        moved = True
    elif keys[pygame.K_d]:
        dx = 1
        direction = "right"
        moved = True

    # Update posisi karakter
    new_x = x + dx * speed * dt
    new_y = y + dy * speed * dt
    
    if inside_house:
        # Batasan dalam rumah
        interior_bounds = pygame.Rect(0, 0, 336, 236)  # 400-64, 300-64
        if interior_bounds.collidepoint(new_x, new_y):
            x, y = new_x, new_y
    else:
        # Batasan luar rumah
        if 0 <= new_x <= 736 and 0 <= new_y <= 536:  # 800-64, 600-64
            x, y = new_x, new_y

    # Update pohon
    for tree in trees:
        tree.update()

    # Timer animasi
    if moved:
        if animation_timer >= walk_animation_speed:
            animation_timer = 0
            frame_index = (frame_index + 1) % 2
    else:
        if animation_timer >= idle_animation_speed:
            animation_timer = 0
            frame_index = (frame_index + 1) % 2

    # Ambil frame animasi aktif
    if has_tool:
        sprite_list = tool_sprites.get(direction, tool_sprites["down"])
        frame = sprite_list[1] if using_tool else sprite_list[frame_index]
    else:
        if moved:
            if direction == "up":
                frame = walk_up_frames[frame_index]
            elif direction == "down":
                frame = walk_down_frames[frame_index]
            elif direction == "left":
                frame = walk_left_frames[frame_index]
            elif direction == "right":
                frame = walk_right_frames[frame_index]
        else:
            frame = idle_frames[direction][frame_index]

    # Render game
    if inside_house:
        # Gambar latar dalam rumah
        screen.fill((0, 0, 0))
        screen.blit(interior_bg, (0, 0))

        # Gambar furnitur jika tersedia
        if bed_img:
            screen.blit(bed_img, furniture_positions["bed"])
        if table_img:
            screen.blit(table_img, furniture_positions["table"])
        if chair_img:
            screen.blit(chair_img, furniture_positions["chair"])
        if sofa_img:
            screen.blit(sofa_img, furniture_positions["sofa"])

        # Info dalam rumah
        font = pygame.font.Font(None, 36)
        text = font.render("Di dalam rumah", True, (0, 0, 0))
        screen.blit(text, (20, 10))
    else:
        # Gambar latar outdoor
        screen.fill((107, 142, 35))  # Olive green

        # Gambar pohon dan buah-buahnya
        for tree in trees:
            tree.draw(screen, tree_img)

        # Gambar batang pohon
        if stump_img:
            for pos in outdoor_furniture.get("stump", []):
                screen.blit(stump_img, pos)

        # Gambar semak
        if bush_img:
            for pos in outdoor_furniture.get("bush", []):
                screen.blit(bush_img, pos)

        # Gambar rumah
        if house_sprite:
            screen.blit(house_sprite, (house_x, house_y))
        
        # Tampilkan instruksi masuk rumah jika dekat
        if check_house_collision(x, y):
            font = pygame.font.Font(None, 24)
            text = font.render("Tekan F untuk masuk rumah", True, (255, 255, 0))
            screen.blit(text, (house_x - 20, house_y - 30))

        # Tampilkan instruksi panen jika dekat pohon berbuah
        for tree in trees:
            if tree.is_near((x, y)) and tree.has_available_fruits():
                font = pygame.font.Font(None, 24)
                available_count = sum(tree.available_fruits)
                text = font.render(f"Tekan ENTER untuk panen buah ({available_count} tersisa)", True, (255, 255, 0))
                screen.blit(text, (tree.pos[0] - 80, tree.pos[1] - 30))
                break

    # Gambar karakter
    screen.blit(frame, (round(x), round(y)))

    # Gambar UI
    draw_inventory()
    draw_instructions()

    # Tampilkan frame
    pygame.display.flip()

# Keluar dari Pygame
pygame.quit()
sys.exit()