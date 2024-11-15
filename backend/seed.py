from src.seeders.province_seeder import seed_provinces

def main():
    print("🌱 Starting to seed provinces...")
    seed_provinces()
    print("✅ Province seeding completed!")

if __name__ == "__main__":
    main()