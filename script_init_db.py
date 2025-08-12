import subprocess
import psycopg2
from psycopg2 import sql
from app.db.session import SessionLocal
from app.models import user, product
from app.db.init_db import init_db
from dotenv import load_dotenv
import os
import sys
import time

load_dotenv(dotenv_path="./.env")

# Fetch environment variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def reset_alembic_version():
    """Reset alembic version table"""
    print("\n🔄 Resetting Alembic version table...")
    try:
        import sqlalchemy
        from sqlalchemy import create_engine, text
        
        # Construct the database URL
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        
        # Create engine
        engine = create_engine(DATABASE_URL)
        
        # Reset alembic version table
        with engine.connect() as connection:
            # Check if alembic_version table exists
            result = connection.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'alembic_version'
                )
            """))
            table_exists = result.scalar()
            
            if table_exists:
                connection.execute(text("DELETE FROM alembic_version"))
                connection.commit()
                print("✅ Alembic version table reset successfully!")
            else:
                print("ℹ️  Alembic version table doesn't exist yet (normal for fresh database).")
        return True
    except Exception as e:
        print(f"❌ Failed to reset alembic version: {e}")
        return False

def run_alembic_revision():
    """Run alembic revision --autogenerate"""
    print("\n🔄 Generating Alembic migration...")
    try:
        result = subprocess.run(
            "alembic revision --autogenerate -m \"Initial migration\"", 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Alembic migration generated successfully!")
            if result.stdout:
                print(f"Output: {result.stdout}")
            return True
        else:
            # Check if the error is about no changes to migrate
            if "No changes in schema detected" in result.stderr or "No changes in schema detected" in result.stdout:
                print("ℹ️  No schema changes detected - this is normal if tables already exist")
                return True
            else:
                print(f"❌ Failed to generate migration: {result.stderr}")
                return False
    except Exception as e:
        print(f"❌ Error generating migration: {e}")
        return False

def stamp_current_migration():
    """Stamp the current migration"""
    print("\n🔄 Stamping current migration...")
    try:
        result = subprocess.run(
            "alembic stamp head", 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Current migration stamped successfully!")
            return True
        else:
            print(f"❌ Failed to stamp migration: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error stamping migration: {e}")
        return False

def run_alembic_upgrade():
    """Run alembic upgrade head"""
    return run_command(
        "alembic upgrade head",
        "Applying Alembic migrations"
    )

def seed_database():
    """Seed the database with sample data"""
    print("\n🔄 Seeding database with sample data...")
    try:
        db = SessionLocal()

        # Clear existing data first
        db.query(product.Product).delete()
        db.query(user.User).delete()
        db.commit()
        print("✅ Existing data cleared.")

        # Insert sample users
        user1 = user.User(name="John Doe", email="johndoe@example.com", role="user")
        user2 = user.User(name="Khánh Trần", email="khanhtran@gohub.com", role="admin")

        db.add(user1)
        db.add(user2)

        # Insert sample products with correct enum values
        product1 = product.Product(
            product_code="THADTF",
            status=product.ProductStatus.ACTIVE,  # Will store "active" in DB
            type_of_sim=product.SimType.SIM,      # Will store "SIM" in DB
            operator_code=product.OperatorCode.DTAC,  # Will store "DTAC" in DB
            vendor_code=product.VendorCode.DTAC,      # Will store "DTAC" in DB
            purchase_type=product.PurchaseType.API_PURCHASE,  # Will store "API Purchase" in DB
            sku_type=product.SkuType.BASE,           # Will store "Base" in DB
            data_type=product.DataType.FIXED_DATA,   # Will store "Fixed Data" in DB
            hotspot=True
        )
        product2 = product.Product(
            product_code="EUSAJYP",
            status=product.ProductStatus.ACTIVE,     # Will store "active" in DB
            type_of_sim=product.SimType.E_SIM,       # Will store "eSIM" in DB
            operator_code=product.OperatorCode.JY,   # Will store "JOYTEL" in DB
            vendor_code=product.VendorCode.KANGO,    # Will store "KANGO" in DB
            purchase_type=product.PurchaseType.API_PURCHASE,  # Will store "API Purchase" in DB
            sku_type=product.SkuType.BASE_DATAPACK,  # Will store "Base + Datapack" in DB
            data_type=product.DataType.DAILY_DATA,   # Will store "Daily Data" in DB
            hotspot=False
        )

        db.add(product1)
        db.add(product2)

        db.commit()
        db.close()

        print("✅ Sample data inserted successfully!")
        print("✅ Enum values now stored correctly (e.g., 'active' instead of 'ACTIVE')")
        return True
    except Exception as e:
        print(f"❌ Failed to seed database: {e}")
        return False

def main():
    """Main function to run all database initialization steps"""
    print("🚀 Starting database initialization...")
    print("=" * 50)
    
    # Step 1: Reset alembic version table
    if not reset_alembic_version():
        print("❌ Failed to reset alembic version. Exiting.")
        sys.exit(1)
    
    # Step 2: Stamp current migration
    if not stamp_current_migration():
        print("❌ Failed to stamp current migration. Exiting.")
        sys.exit(1)
    
    # Step 3: Generate new migration (if needed)
    if not run_alembic_revision():
        print("❌ Failed to generate migration. Exiting.")
        sys.exit(1)
    
    # Step 4: Apply migration
    if not run_alembic_upgrade():
        print("❌ Failed to apply migration. Exiting.")
        sys.exit(1)
    
    # Step 5: Seed database
    if not seed_database():
        print("❌ Failed to seed database. Exiting.")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Database initialization completed successfully!")
    print("✅ Alembic migration generated and applied")
    print("✅ Database seeded with sample data")
    print("✅ Ready to run your application!")

if __name__ == "__main__":
    main()
