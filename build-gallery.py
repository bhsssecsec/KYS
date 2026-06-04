#!/usr/bin/env python3
"""
Build student gallery HTML with all classes
Run this script whenever you add new student folders
"""

import os
import base64
import json
import re
import sys

def process_folder(folder_name, class_name):
    """Process images from a folder"""
    folder_path = os.path.join(os.getcwd(), folder_name)
    
    if not os.path.isdir(folder_path):
        return []
    
    image_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.jpg')])
    students = []
    
    print(f"  Processing {folder_name}/ ({len(image_files)} images)...", end=" ")
    
    for filename in image_files:
        filepath = os.path.join(folder_path, filename)
        roll_no = None
        
        # Extract roll number from filename
        if filename.startswith(tuple('0123456789')):
            match = re.match(r'(\d+)_', filename)
            if match:
                roll_no = int(match.group(1))
        else:
            match = re.search(r'_(\d+)\.jpg', filename)
            if match:
                roll_no = int(match.group(1))
        
        if not roll_no:
            continue
        
        with open(filepath, 'rb') as f:
            img_data = base64.b64encode(f.read()).decode()
        
        student = {
            "rollNo": roll_no,
            "class": class_name,
            "name": f"Student {roll_no}",
            "photo": f"data:image/jpeg;base64,{img_data}"
        }
        students.append(student)
    
    print(f"✓ {len(students)} added")
    return students

def main():
    print("🎓 Building Student Gallery...\n")
    
    # Define class folders to process
    class_folders = [
        ("IXA", "IX A"),
        ("IXB", "IX B"),
        ("IXC", "IX C"),
        ("XA", "X A"),
        ("XB", "X B"),
    ]
    
    all_students = []
    
    print("Scanning folders:")
    for folder, class_name in class_folders:
        students = process_folder(folder, class_name)
        all_students.extend(students)
    
    if not all_students:
        print("\n❌ No students found! Check your folder structure.")
        sys.exit(1)
    
    # Sort by class and roll number
    all_students.sort(key=lambda x: (x['class'], x['rollNo']))
    
    print(f"\nProcessed {len(all_students)} total students")
    
    # Print summary
    classes = {}
    for s in all_students:
        if s['class'] not in classes:
            classes[s['class']] = 0
        classes[s['class']] += 1
    
    print("\nClasses:")
    for cls in sorted(classes.keys()):
        print(f"  {cls}: {classes[cls]} students")
    
    # Read HTML template
    with open('student-gallery.html', 'r') as f:
        template = f.read()
    
    # Embed data into template
    students_json = json.dumps(all_students)
    html = template.replace(
        'const students = [];',
        f'const students = {students_json};'
    )
    
    # Write complete HTML
    with open('student-gallery-complete.html', 'w') as f:
        f.write(html)
    
    size_mb = os.path.getsize('student-gallery-complete.html') / (1024*1024)
    print(f"\n✅ Created student-gallery-complete.html ({size_mb:.1f} MB)")
    print("\nOpen it:")
    print("  http://localhost:8000/student-gallery-complete.html")

if __name__ == '__main__':
    main()
