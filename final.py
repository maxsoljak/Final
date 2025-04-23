from abc import ABC, abstractmethod
import re 

# This is my abstract class, it forces child classes jobseeker, employer to use their own version of display_menu().
class User(ABC):
    def __init__(self, username, password):
        self._account = Account(username, password)  

    @abstractmethod
    def display_menu(self):
        pass

    def authenticate(self, username, password):
        return self._account.get_username() == username and self._account.check_password(password)

# Classes for skills, profiles, account etc.
class Account:
    def __init__(self, username, password):
        self._username = username
        self._password = password

    def get_username(self): #method for returning username
        return self._username

    def check_password(self, password): 
        return self._password == password

class Skill:
    def __init__(self, id, name): #gives perticular skill a number
        self._id = id
        self._name = name

    
    def __str__(self):
        return f"{self._id}. {self._name}" # prints skills like 1 is hardworking


class SkillSet:
    def __init__(self):
        self._skills = [    #list of different popular skills user will choose 5 both employer and job seeker
            Skill(1, "Hardworking"),
            Skill(2, "Communication"),
            Skill(3, "Teamwork"),
            Skill(4, "Problem-Solving"),
            Skill(5, "Adaptability"),
            Skill(6, "Creativity"),
            Skill(7, "Leadership"),
            Skill(8, "Time Management"),
            Skill(9, "Attention to Detail"),
            Skill(10, "Multitasking"),
            Skill(11, "Critical Thinking"),
            Skill(12, "Flexibility"),
            Skill(13, "Technical Proficiency")
        ]

    def display_skills(self):   #the skill menu by name fn
        print("Available skills:")
        for skill in self._skills:
            print(skill)

    def get_skill_by_id(self, skill_id):  #the program find a specific skill from the list based on the numbe
        for skill in self._skills:
            if skill._id == skill_id:
                return skill
        return None

class Profile:
    def __init__(self, username):
        self._username = username
        self._skills = []
        self._status = "Pending" #If not chosen by no employer yet
        self._accepted_by = None  #room for name if accapted by employer
        self._contact_info = None #employer will provide  US phone number

    def add_skill(self, skill):
        if skill not in self._skills:  #if not in our skills yet add it 
            self._skills.append(skill)

    def get_skills(self):
        return self._skills #all 5 skills

    def update_status(self, new_status): 
        self._status = new_status

    def set_acceptance_details(self, employer_username, contact_info): #defintion for job seeker if he selects status of application
        self._accepted_by = employer_username
        self._contact_info = contact_info
        self._status = "Accepted"

    def get_status(self):   
        return self._status

    def get_acceptance_info(self): #this is for accapted
        return self._accepted_by, self._contact_info

    def clear_skills(self): #when creating new application
        self._skills = []
        self._status = "Pending"
        self._accepted_by = None
        self._contact_info = None

    def __str__(self):
        skills = ", ".join(str(skill) for skill in self._skills)
        
        status_info = f"Application Status: {self._status}"
       
        if self._status == "Accepted" and self._accepted_by:
            
            status_info += f"\nAccepted by: {self._accepted_by}\nContact: {self._contact_info}" 
        
        return f"Username: {self._username}\nSkills: {skills}\n{status_info}"

class MatchResult:
    def __init__(self, seeker_username, match_count):
        self.seeker_username = seeker_username
        self.match_count = match_count

    def __str__(self):
        return f"{self.seeker_username}: {self.match_count} / 5 skill(s) matched" #for employer to see how many skill have in common with job seeker

class Validator:
    @staticmethod
    def validate_username(username):
        return username.isalnum() and len(username) >= 3 #just to make sure username is not too short

    @staticmethod
    def validate_password(password): #just to make sure username is not too short
        return len(password) > 0

    @staticmethod
    def validate_phone(phone):
        return bool(re.fullmatch(r"\d{10}", phone)) #to make sure the phone number has 10 digits (US)

class Database:  #using this to navigage between profiles and saving it
    def __init__(self):
        self.users = []
        self.job_seekers = []
        self.employers = []

    def add_user(self, user):
        self.users.append(user)
        
        if isinstance(user, JobSeeker):
            self.job_seekers.append(user) #adding job seekere to databse user
        
        elif isinstance(user, Employer): #adding emplyer to databse user
            self.employers.append(user)

    def find_user(self, role, username, password):
        
        candidates = self.job_seekers if role == "job_seeker" else self.employers
        
        for user in candidates: #if job seeker or emplyer check for password and username and return their user. This keeps employers and job seekers seperated
            if user.authenticate(username, password):
                return user
        return None

class JobSeeker(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.profile = Profile(username)

    def create_profile(self, skillset):
        self.profile.clear_skills() #Just for beggining first log
        print("Select 5 skills by entering numbers (1 to 13):")
        
        selected_ids = set()
        
        while len(selected_ids) < 5:
            skillset.display_skills()
            choice = input(f"Select skill {len(selected_ids) + 1}: ")
            
            if choice.isdigit():
                skill_id = int(choice)
                
                if skill_id in selected_ids:
                    print("You already selected that skill.") #if already in skills print this
                    continue
                
                skill = skillset.get_skill_by_id(skill_id)
                
                if skill:
                    self.profile.add_skill(skill)
                    selected_ids.add(skill_id)
                else:
                    print("Invalid choice. Try again.")
            else:
                print("Please enter a number.")
        print("Your profile was created!")
        print(self.profile)

    def display_menu(self, skillset):
        print(f"\nWelcome, {self._account.get_username()} (Job Seeker)")
        
        if not self.profile.get_skills():
            self.create_profile(skillset) 
        else:
            print("Your current application status is:", self.profile.get_status())
            print("1. View profile")
            print("2. Create new application")
            choice = input("Choose an option: ")
            if choice == "1":
                print(self.profile)
            
            elif choice == "2":
                self.create_profile(skillset) #start again and add skills again

class Employer(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.required_profile = Profile(username)

    def define_required_skills(self, skillset):
        print("Pick 5 skills you're looking for in candidates:")
        selected_ids = set()
        while len(selected_ids) < 5:
            skillset.display_skills()
            choice = input(f"Select skill {len(selected_ids) + 1}: ")
            
            if choice.isdigit():
                skill_id = int(choice)
                if skill_id in selected_ids:
                    print("You already selected that skill.")
                    continue
                skill = skillset.get_skill_by_id(skill_id)
                
                if skill:
                    self.required_profile.add_skill(skill)
                    selected_ids.add(skill_id)
                else:
                    print("Invalid skill ID.")
            else:
                print("Please enter a number.")
        print("Your required skills is saved.")

    def list_matches(self, job_seekers):
        print(f"\nHere are job seekers that match your preferences:")
        
        for seeker in job_seekers:
            seeker_skills = seeker.profile.get_skills() #looping through candidates with skills
            
            match_count = sum(skill in self.required_profile.get_skills() for skill in seeker_skills)
            
            result = MatchResult(seeker.profile._username, match_count) #matching us with job seekers
            
            print(result)

    def pick_applicant(self, job_seekers):
        username = input("Type the username of a job seeker you'd like to accept: ")
        
        for seeker in job_seekers:
            if seeker.profile._username == username:
                phone = input("Enter your phone number (10 digits): ") #asked after selecting job seeker
                
                if Validator.validate_phone(phone):
                    seeker.profile.set_acceptance_details(self._account.get_username(), phone)
                    print(f"You accepted {username}!")
                else:
                    print("Invalid phone number format. Must be 10 digits.")
                return
        print("No matching job seeker found.")

    def display_menu(self, skillset, job_seekers):
        print(f"\nWelcome, {self._account.get_username()} (Employer)")
        self.define_required_skills(skillset)
        self.list_matches(job_seekers)
        self.pick_applicant(job_seekers)

class Menu:
    def __init__(self):
        self.db = Database()
        self.skillset = SkillSet()

    def run(self):
        while True:
            print("\n      =====================      ")
            print("\n=====   Job Matching.com    =====")
            print("\n      =====================      ")
            print("1. Sign up as Job Seeker")
            print("2. Sign up as Employer")
            print("3. Log in as Job Seeker")
            print("4. Log in as Employer")
            print("5. Exit")

            choice = input("Choose an option: ")

            if choice == "1":
                self.create_user("job_seeker")
            elif choice == "2":
                self.create_user("employer")
            elif choice == "3":
                self.login_user("job_seeker")
            elif choice == "4":
                self.login_user("employer")
            elif choice == "5":
                print("Thanks for using the Job Matching!")
                break
            else:
                print("Invalid option. Please choose again.")

    def create_user(self, role):
        username = input("Choose a username: ")
        password = input("Choose a password: ")
        if not Validator.validate_username(username) or not Validator.validate_password(password):
            print("Username must be at least 3 letters. Password cannot be empty.")
            return

        if role == "job_seeker":
            user = JobSeeker(username, password)
        else:
            user = Employer(username, password)

        self.db.add_user(user)
        print(f"Your {role.replace('_', ' ').title()} profile has been created.") #If employer or job seeker created profile

    def login_user(self, role):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        user = self.db.find_user(role, username, password)
        if user:
            if role == "job_seeker":
                user.display_menu(self.skillset)
            else:
                user.display_menu(self.skillset, self.db.job_seekers)
        else:
            print("Sorry, password or username didn't match any account.")

if __name__ == "__main__":
    app = Menu()
    app.run()