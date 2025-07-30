import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Database credentials from .env
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME") 

def run_sql_script(sql_script_content):
    """
    Connects to MySQL and executes the provided SQL script.
    It first connects without a specific database to create it,
    then connects to the newly created database to execute further statements.
    """
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )

        cursor = conn.cursor()

        # Split the script into individual statements
        # This simple split works for most cases, but be careful with
        # complex statements containing semicolons within strings or comments.
        statements = [s.strip() for s in sql_script_content.split(';') if s.strip()]

        # Execute statements
        for statement in statements:
            if statement.lower().startswith("create database"):
                try:
                    cursor.execute(statement)
                    print(f"Executed: {statement[:50]}...")
                    # Once the database is created, close the current connection
                    # and reconnect to the new database
                    cursor.close()
                    conn.close()
                    
                    # Reconnect to the newly created database
                    conn = mysql.connector.connect(
                        host=DB_HOST,
                        user=DB_USER,
                        password=DB_PASSWORD,
                        database=DB_NAME # Connect to the specific database
                    )
                    cursor = conn.cursor()
                    print(f"Successfully connected to database '{DB_NAME}'.")
                except mysql.connector.Error as err:
                    if err.errno == 1007: # Error code for "Can't create database; database exists"
                        print(f"Database '{DB_NAME}' already exists. Connecting to it.")
                        # If database exists, just connect to it and continue
                        cursor.close()
                        conn.close()
                        conn = mysql.connector.connect(
                            host=DB_HOST,
                            user=DB_USER,
                            password=DB_PASSWORD,
                            database=DB_NAME
                        )
                        cursor = conn.cursor()
                    else:
                        print(f"Error creating database: {err}")
                        raise # Re-raise other errors
            else:
                try:
                    cursor.execute(statement)
                    # print(f"Executed: {statement[:50]}...") # Uncomment for more verbose output
                except mysql.connector.Error as err:
                    print(f"Error executing statement: {statement[:100]}...")
                    print(f"Error: {err}")
                    # You might want to break or raise here depending on your error handling needs
        
        conn.commit() # Commit all changes
        print("\nSQL script executed successfully.")

    except mysql.connector.Error as err:
        print(f"Error connecting to database or executing query: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    sql_script = """
    create table if not exists navtable(
    nav_id int auto_increment primary key,
    navLogo varchar(200),
    navAnchor1 varchar(200),
    navAnchor2 varchar(200),
    navAnchor3 varchar(200),
    dropdown1 varchar(200),
    dropdown2 varchar(200),
    navbtn varchar(200)
    );
    INSERT INTO navtable (navLogo, navAnchor1, navAnchor2, navAnchor3, dropdown1, dropdown2, navbtn )
    VALUES ('static/assets/images/navlogo.png', 'Our Solutions','FAQs', 'Contact','Match Making(Live Now)','Upcomming Solutions(Comming Solutions)','Book Demo');

    create table if not exists  herotable(
    hero_id int auto_increment primary key,
    heroHeading varchar(200),
    heroDescription varchar(1000),
    heroImg varchar(200)

    );

    INSERT INTO herotable (heroHeading, heroDescription, heroImg )
    VALUES ('De-Risking Human Progress', 'With elite insurance expertise empowered by breakthrough technology, Newfront is the modern insurance brokerage for the 21st century.', 'static/assets/images/hero.png');

    create Table if not exists  clientTrust(
    clientTrust_id int auto_increment primary key,
    clientHeading varchar(200),
    clientDescription varchar(1000), clientImg1 varchar(200), clientImg2 varchar(200), clientImg3 varchar(200), clientImg4 varchar(200),
    clientImg5 varchar(200), clientImg6 varchar(200), clientImg7 varchar(200), clientImg8 varchar(200), clientImg9 varchar(200)
    );

    INSERT INTO clientTrust (clientHeading, clientDescription ,clientImg1, clientImg2, clientImg3, clientImg4, clientImg5, clientImg6, clientImg7, clientImg8, clientImg9)
    VALUES ('Clients Trust Newfront', 'Our experts consult with companies across all growth stages on strategies that align with their benefits philosophy.', 'static/assets/images/client1.png', 'static/assets/images/client2.webp', 'static/assets/images/client3.png', 'static/assets/images/client4.webp', 'static/assets/images/client5.png', 'static/assets/images/client6.png', 'static/assets/images/client7.webp', 'static/assets/images/client8.png', 'static/assets/images/client9.webp');



    create table if not exists  innovationTable(
    innovation_id int auto_increment primary key,
    innovationHeadTop varchar(200), innovationHeadmain varchar(200), innovationDescription varchar(200),
    li1 varchar(1000), li2 varchar(1000), li3 varchar(1000), li4 varchar(1000),
    innovationVideo varchar(500)
    );
    INSERT INTO innovationTable (innovationHeadTop, innovationHeadmain ,innovationDescription, li1, li2, li3, li4, innovationVideo)
    VALUES ('Impactful Innovation','Charting a New Course','We’re bringing advanced technology to an antiquated industry, fostering transparency, convenience, and optimized client outcomes.','Business insurance clients can have 24/7 access to their entire insurance program including policies, losses, COIs, and billing, on any device through Newfront’s connected dashboard','Total rewards clients can access benefit plans, compliance information, and secure documents in our centralized platform','Predictive analytics and proprietary benchmarking enable better carrier negotiations and informed decision-making','Multiple AI-enabled technology solutions continue to be developed, saving clients time and improving their experiences','static/assets/videos/a_new_course.webm');

    create table if not exists  clientExperience(
    clientExp_id int auto_increment primary key,
    clientExpHead varchar(200),
    clientExpDescription varchar(1000),
    clientExpVideo varchar(500)
    );
    INSERT INTO clientExperience (clientExpHead, clientExpDescription ,clientExpVideo)
    VALUES ('Using AI to Improve the Client Experience', 'Newfront is building breakthrough AI to drive client insights and free our teams to do the strategic work they were built to do.', 'static/assets/videos/improve-experience.webm');

    create table if not exists  statistics(
    statistics_id int auto_increment primary key,
    statHead varchar(200),
    statDescription varchar(200)
    );
    INSERT INTO statistics (statHead, statDescription)
    VALUES ('By the Numbers', 'The data speaks for itself. From our large roster of established and growing clients to our stellar client retention rate—we build relationships that last.');

    create table if not exists  stat_card(
    statCard_id int auto_increment primary key,
    StatcardLogo1 varchar(500), StatcardLogo2 varchar(500), StatcardLogo3 varchar(500),
    StatcardHead1 varchar(500), StatcardHead2 varchar(500), StatcardHead3 varchar(500),
    StatcardPara1 varchar(500), StatcardPara2 varchar(500), StatcardPara3 varchar(500)
    );

    INSERT INTO stat_card (StatcardLogo1, StatcardLogo2,StatcardLogo3,StatcardHead1,StatcardHead2,StatcardHead3,StatcardPara1,StatcardPara2,StatcardPara3)
    VALUES ('static/assets/images/stats1.png','static/assets/images/stats2.png','static/assets/images/stats3.png','$3.1B','~20%','500+','in annual premiums placed','U.S. unicorns represented','public company experience');

    create table if not exists  getToKnow(
    knowId int auto_increment primary key,
    knowHead varchar(200), knowVideo varchar(500)
    );
    insert into getToKnow values(1,'Get to Know Fortifund','static/assets/videos/get-to-know.webm');

    create table if not exists  exploreTable(
    explore_id INT AUTO_INCREMENT PRIMARY KEY,
    exploreHeading varchar(200)
    );
    INSERT INTO exploreTable (exploreHeading)
    VALUES ('Explore Our Industries and Services');

    create table if not exists  footer(
    footer_id INT AUTO_INCREMENT PRIMARY KEY,
    footer_logo varchar(200),
    footer_social_icon1 varchar(200),
    footer_social_icon2 varchar(200),
    footer_social_icon3 varchar(200),
    footer_social_icon4 varchar(200),
    footer_social_link1 varchar(200),
    footer_social_link2 varchar(200),
    footer_social_link3 varchar(200),
    footer_social_link4 varchar(200)
    );
    UPDATE footer
    SET footer_logo = 'static/assets/images/footerLogo.png',
        footer_social_icon1 = 'static/assets/images/fbimg.png',
        footer_social_icon2 = 'static/assets/images/image.png',
        footer_social_icon3 = 'static/assets/images/insta.png',
        footer_social_icon4 = 'static/assets/images/twitter.png'
    WHERE footer_id = 1;

    INSERT INTO footer (footer_logo, footer_social_icon1,  footer_social_icon2, footer_social_icon3 , footer_social_icon4, footer_social_link1, footer_social_link2, footer_social_link3, footer_social_link4 )
    VALUES ('static/assets/images/footerLogo.png', 'static/assets/images/fbimg.png', 'static/assets/images/image.png', 'static/assets/images/insta.png', 'static/assets/images/twitter.png', '#', '#', '#', '#');

    CREATE TABLE IF NOT EXISTS Images (
        image_id INT AUTO_INCREMENT PRIMARY KEY,
        image_filename VARCHAR(255) NOT NULL UNIQUE,
        alt_text VARCHAR(500),
        upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS Blogs (
        blog_id INT AUTO_INCREMENT PRIMARY KEY,
        heading VARCHAR(255) NOT NULL,
        subheading VARCHAR(500),
        author VARCHAR(100) NOT NULL,
        publish_date DATE NOT NULL,
        content TEXT NOT NULL,
        thumbnail_image_id INT,
        FOREIGN KEY (thumbnail_image_id) REFERENCES Images(image_id) ON DELETE SET NULL
    );

    CREATE TABLE contact_submissions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        job_title VARCHAR(255),
        company_name VARCHAR(255),
        phone_number VARCHAR(50),
        email VARCHAR(255) UNIQUE NOT NULL,
        industry VARCHAR(255),
        num_employees VARCHAR(50), -- Storing as VARCHAR as input type is text
        additional_details TEXT,
        submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE contact_submissions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        job_title VARCHAR(255),
        company VARCHAR(255),
        email VARCHAR(255) NOT NULL,
        phone VARCHAR(255),
        message TEXT,
        submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    INSERT INTO navtable (navLogo, navAnchor1, navAnchor2, navAnchor3, dropdown1, dropdown2, navbtn)
    VALUES ('static/assets/images/navlogo.png', 'Our Solution', 'FAQs', 'Connect', 'Match making (Live Now)', 'Upcomming Solutions (Comming Soon)', 'Book Demo');

    CREATE TABLE faqs (
        faq_id INT AUTO_INCREMENT PRIMARY KEY,
        category VARCHAR(255) NOT NULL,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE contact_submissions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        job_title VARCHAR(255),
        company_name VARCHAR(255),
        phone_number VARCHAR(50),
        email VARCHAR(255) NOT NULL,
        industry VARCHAR(255),
        num_employees VARCHAR(50),
        additional_details TEXT,
        submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS AdminSettings (
        setting_name VARCHAR(255) PRIMARY KEY,
        setting_value TEXT NOT NULL
    );

     CREATE TABLE demo_bookings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        firm_name VARCHAR(255),
        company_type VARCHAR(100),
        person_name VARCHAR(255),
        title VARCHAR(100),
        email VARCHAR(255),
        team_size VARCHAR(50),
        meeting_date DATE,
        meeting_time VARCHAR(20),
        meeting_link VARCHAR(500),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
     );

    -- Insert General Questions
    INSERT INTO faqs (category, question, answer) VALUES
    ('General Questions', 'What is FortiFund?', 'FortiFund is a deal-matching platform that connects brokered deals to the right lenders based on underwriting criteria — automatically, efficiently, and securely. It is not a CRM.'),
    ('General Questions', 'How is FortiFund different from a CRM?', 'CRMs help manage contacts and communication. FortiFund helps you close more deals by matching submissions with lenders that actually fund your deals — without the admin hassle.'),
    ('General Questions', 'Who can use FortiFund?', 'Brokers and processors looking to submit deals faster and smarter, and lenders searching for deals that meet their funding criteria.');

    -- Insert For Brokers Questions
    INSERT INTO faqs (category, question, answer) VALUES
    ('For Brokers', 'Can I choose which lenders I work with?', 'Yes! Each brokerage can customize their back end to prioritize preferred lenders — including those who offer the highest commissions or who you’ve worked with before.'),
    ('For Brokers', 'How do I submit a deal?', 'Log in, complete the short intake form, and drag-and-drop your files. FortiFund matches your deal with lenders based on both your preferences and lender guidelines.'),
    ('For Brokers', 'Are deals automatically sent to lenders?', 'Not yet — but we’re getting there. Right now, FortiFund matches your deal with the most relevant lenders based on their criteria and your preferences. Once matched, you’ll still send the deal to the lender yourself, just like you normally would — but with more confidence that it’s the right fit. We’re actively working on features that will let you send and track deals directly through the platform.'),
    ('For Brokers', 'Can I prioritize lenders based on commission payouts?', 'Yes. FortiFund allows you to rank lenders based on your priorities, including commission structures. Our system takes that into account when suggesting matches.'),
    ('For Brokers', 'How much does it cost to use FortiFund?', 'We offer flexible pricing — pay-per-deal or monthly plans. Contact us for a package tailored to your volume.');

    -- Insert For Lenders Questions
    INSERT INTO faqs (category, question, answer) VALUES
    ('For Lenders', 'What kind of deals will I see?', 'Only those that match your guidelines. You’ll only see deals worth your time — and without any clutter.'),
    ('For Lenders', 'Can I set custom deal preferences?', 'Yes. You can define your underwriting rules, industries, revenue ranges, and more — and update them anytime.'),
    ('For Lenders', 'Will I get repeat low-quality deals?', 'No. Brokers only send deals that match your preferences, and we prioritize quality over volume.');

    -- Insert Security & Privacy Questions
    INSERT INTO faqs (category, question, answer) VALUES
    ('Security & Privacy', 'Is my data safe on FortiFund?', 'Yes. Your deal data is stored securely, and sensitive client information is kept private. Only you control who ultimately receives the full details. We’re also building features to improve tracking and data security even further.'),
    ('Security & Privacy', 'Will my deals be sent to all lenders?', 'No. FortiFund doesn’t blast your deals out. Instead, we use precision matching to identify the single best-fit lender for each deal — based on underwriting criteria, your preferences, and even commission structures. This gives you the confidence to send your deal to just one lender, which: Increases your chance of getting the deal funded, Helps you earn the highest commissions possible, and Eliminates the risk of your deal being backdoored or overexposed. You stay in full control — once you receive a match, you send the deal directly, just like you normally would.');

    -- Insert Support & Customization Questions
    INSERT INTO faqs (category, question, answer) VALUES
    ('Support & Customization', 'Can I get help tailoring FortiFund to my workflow?', 'Yes! Our team will work with you to configure your dashboard, deal settings, and lender preferences to fit your business goals.'),
    ('Support & Customization', 'What if I need help with a hard-to-place deal?', 'We’re here to help. Our team and tools are designed to find the right match — even for deals that don’t fit the standard mold.');
    """
    
if __name__ == "__main__":
    run_sql_script(sql_script)