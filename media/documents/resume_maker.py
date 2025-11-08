import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from fpdf import FPDF
from tkinter import ttk

def save_resume(details):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Helper function to draw a footer line
    def draw_footer_line():
        pdf.ln(5)  # Add some vertical space
        pdf.set_draw_color(200, 200, 200)  # Light gray color
        pdf.set_line_width(0.5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())  # Horizontal line from left to right margin
        pdf.ln(5)  # Add some vertical space after the line

    # Header
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(0, 10, details['name'], ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, details['contact'], ln=True, align="C")
    pdf.cell(0, 10, details['address'], ln=True, align="C")
    pdf.cell(0, 10, details['linkedin'], ln=True, align="C")
    draw_footer_line()

    # Professional Summary
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, "Professional Summary", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, details['summary'])
    draw_footer_line()

    # Education
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, "Education", ln=True)
    pdf.set_font("Arial", size=12)
    for degree, institution, year in details['education']:
        pdf.cell(0, 10, f"{degree} - {institution} ({year})", ln=True)
    draw_footer_line()

    # Work Experience
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, "Work Experience", ln=True)
    pdf.set_font("Arial", size=12)
    for job_title, company, years, description in details['experience']:
        pdf.cell(0, 10, f"{job_title} at {company} ({years})", ln=True)
        pdf.multi_cell(0, 10, f"- {description}")
    draw_footer_line()

    # Skills
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, "Skills", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, ', '.join(details['skills']))
    draw_footer_line()

    # Save the PDF
    pdf_file_name = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if pdf_file_name:
        pdf.output(pdf_file_name)
        messagebox.showinfo("Success", f"Resume saved as {pdf_file_name}")

def add_education():
    degree = education_degree_entry.get()
    institution = education_institution_entry.get()
    year = education_year_entry.get()
    if degree and institution and year:
        education_listbox.insert(tk.END, f"{degree} - {institution} ({year})")
        education_entries.append((degree, institution, year))
        education_degree_entry.delete(0, tk.END)
        education_institution_entry.delete(0, tk.END)
        education_year_entry.delete(0, tk.END)

def add_experience():
    job_title = experience_job_entry.get()
    company = experience_company_entry.get()
    years = experience_years_entry.get()
    description = experience_description_entry.get("1.0", tk.END).strip()
    if job_title and company and years and description:
        experience_listbox.insert(tk.END, f"{job_title} at {company} ({years})")
        experience_entries.append((job_title, company, years, description))
        experience_job_entry.delete(0, tk.END)
        experience_company_entry.delete(0, tk.END)
        experience_years_entry.delete(0, tk.END)
        experience_description_entry.delete("1.0", tk.END)

def generate_resume():
    details = {
        'name': name_entry.get(),
        'contact': contact_entry.get(),
        'address': address_entry.get(),
        'linkedin': linkedin_entry.get(),
        'summary': summary_entry.get("1.0", tk.END).strip(),
        'education': education_entries,
        'experience': experience_entries,
        'skills': skills_entry.get().split(',')
    }
    save_resume(details)

# Initialize the main window
root = tk.Tk()
root.title("Resume Generator")
root.geometry("700x800")
root.configure(bg="#f7f7f7")

# Add a canvas and scrollbar for scrolling
canvas = tk.Canvas(root, bg="#f7f7f7")
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas, padding=10)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

education_entries = []
experience_entries = []

# Title
title_label = tk.Label(scrollable_frame, text="Resume Generator", font=("Arial", 20, "bold"), bg="#f7f7f7", fg="#333")
title_label.pack(pady=10)

# Personal Information Frame
personal_frame = tk.LabelFrame(scrollable_frame, text="Personal Information", font=("Arial", 14), bg="#f7f7f7", fg="#333", padx=10, pady=10)
personal_frame.pack(fill="x", padx=20, pady=10)

tk.Label(personal_frame, text="Full Name:", font=("Arial", 12), bg="#f7f7f7").grid(row=0, column=0, sticky="w", padx=5, pady=5)
name_entry = tk.Entry(personal_frame, width=50)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(personal_frame, text="Contact Information (Phone, Email):", font=("Arial", 12), bg="#f7f7f7").grid(row=1, column=0, sticky="w", padx=5, pady=5)
contact_entry = tk.Entry(personal_frame, width=50)
contact_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(personal_frame, text="Address:", font=("Arial", 12), bg="#f7f7f7").grid(row=2, column=0, sticky="w", padx=5, pady=5)
address_entry = tk.Entry(personal_frame, width=50)
address_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(personal_frame, text="LinkedIn Profile URL:", font=("Arial", 12), bg="#f7f7f7").grid(row=3, column=0, sticky="w", padx=5, pady=5)
linkedin_entry = tk.Entry(personal_frame, width=50)
linkedin_entry.grid(row=3, column=1, padx=5, pady=5)

# Professional Summary Frame
summary_frame = tk.LabelFrame(scrollable_frame, text="Professional Summary", font=("Arial", 14), bg="#f7f7f7", fg="#333", padx=10, pady=10)
summary_frame.pack(fill="x", padx=20, pady=10)

summary_entry = tk.Text(summary_frame, width=70, height=5)
summary_entry.pack(padx=5, pady=5)

# Education Frame
education_frame = tk.LabelFrame(scrollable_frame, text="Education", font=("Arial", 14), bg="#f7f7f7", fg="#333", padx=10, pady=10)
education_frame.pack(fill="x", padx=20, pady=10)

frame_edu_input = tk.Frame(education_frame, bg="#f7f7f7")
frame_edu_input.pack()

tk.Label(frame_edu_input, text="Degree:", font=("Arial", 12), bg="#f7f7f7").grid(row=0, column=0, padx=5, pady=5)
education_degree_entry = tk.Entry(frame_edu_input, width=20)
education_degree_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_edu_input, text="Institution:", font=("Arial", 12), bg="#f7f7f7").grid(row=0, column=2, padx=5, pady=5)
education_institution_entry = tk.Entry(frame_edu_input, width=20)
education_institution_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame_edu_input, text="Year:", font=("Arial", 12), bg="#f7f7f7").grid(row=0, column=4, padx=5, pady=5)
education_year_entry = tk.Entry(frame_edu_input, width=10)
education_year_entry.grid(row=0, column=5, padx=5, pady=5)

add_education_button = tk.Button(frame_edu_input, text="Add", command=add_education, bg="#4caf50", fg="white", font=("Arial", 10, "bold"))
add_education_button.grid(row=0, column=6, padx=5, pady=5)

education_listbox_frame = tk.Frame(education_frame)
education_listbox_frame.pack(fill="x", pady=5)

education_listbox = tk.Listbox(education_listbox_frame, width=80, height=5)
education_listbox.pack(side="left", fill="both", expand=True)

education_scrollbar = ttk.Scrollbar(education_listbox_frame, orient="vertical", command=education_listbox.yview)
education_scrollbar.pack(side="right", fill="y")

education_listbox.configure(yscrollcommand=education_scrollbar.set)

# Work Experience Frame
experience_frame = tk.LabelFrame(scrollable_frame, text="Work Experience", font=("Arial", 14), bg="#f7f7f7", fg="#333", padx=10, pady=10)
experience_frame.pack(fill="x", padx=20, pady=10)

frame_exp_input = tk.Frame(experience_frame, bg="#f7f7f7")
frame_exp_input.pack()

tk.Label(frame_exp_input, text="Job Title:", font=("Arial", 12), bg="#f7f7f7").grid(row=0, column=0, padx=5, pady=5)
experience_job_entry = tk.Entry(frame_exp_input, width=20)
experience_job_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_exp_input, text="Company:", font=("Arial", 12), bg="#f7f7f7").grid(row=0, column=2, padx=5, pady=5)
experience_company_entry = tk.Entry(frame_exp_input, width=20)
experience_company_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame_exp_input, text="Years:", font=("Arial", 12), bg="#f7f7f7").grid(row=0, column=4, padx=5, pady=5)
experience_years_entry = tk.Entry(frame_exp_input, width=10)
experience_years_entry.grid(row=0, column=5, padx=5, pady=5)

tk.Label(frame_exp_input, text="Description:", font=("Arial", 12), bg="#f7f7f7").grid(row=1, column=0, padx=5, pady=5)
experience_description_entry = tk.Text(frame_exp_input, width=50, height=3)
experience_description_entry.grid(row=1, column=1, columnspan=5, padx=5, pady=5)

add_experience_button = tk.Button(frame_exp_input, text="Add", command=add_experience, bg="#4caf50", fg="white", font=("Arial", 10, "bold"))
add_experience_button.grid(row=2, column=5, padx=5, pady=5)

experience_listbox_frame = tk.Frame(experience_frame)
experience_listbox_frame.pack(fill="x", pady=5)

experience_listbox = tk.Listbox(experience_listbox_frame, width=80, height=5)
experience_listbox.pack(side="left", fill="both", expand=True)

experience_scrollbar = ttk.Scrollbar(experience_listbox_frame, orient="vertical", command=experience_listbox.yview)
experience_scrollbar.pack(side="right", fill="y")

experience_listbox.configure(yscrollcommand=experience_scrollbar.set)


# Skills Frame
skills_frame = tk.LabelFrame(scrollable_frame, text="Skills", font=("Arial", 14), bg="#f7f7f7", fg="#333", padx=10, pady=10)
skills_frame.pack(fill="x", padx=20, pady=10)

tk.Label(skills_frame, text="Skills (comma-separated):", font=("Arial", 12), bg="#f7f7f7").pack(anchor="w", padx=5, pady=5)
skills_entry = tk.Entry(skills_frame, width=70)
skills_entry.pack(padx=5, pady=5)

# Final Submit Button
submit_button = tk.Button(scrollable_frame, text="Generate Resume", command=generate_resume, bg="#4caf50", fg="white", font=("Arial", 14, "bold"))
submit_button.pack(pady=20)  # Ensure proper spacing

root.mainloop()
