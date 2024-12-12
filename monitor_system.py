import psutil
import csv 
import argparse
import json

def check_cpu_usage_percentage(interval):
    '''
    checks the cpu usage of system
    Returns --> cpu percentage, type--> float
    '''

    try:
        cpu_percentage = psutil.cpu_percent(interval = interval)
        return {
            "CPU_Percentage" : cpu_percentage
        }
    
    except Exception as e:
        print(f"Error checking CPU usage: {e}")
        return None

def check_memory_usage():
    '''
    checks the memory usage of system

    Parameters --> none
    Returns --> Total/available/used memory, type--> float
    '''
    try:
        memory = psutil.virtual_memory()

        #to the power 3 converts from bytes to gigabytes
        total_memory = memory.total / (1024**3)
        available_memory = memory.available / (1024**3)
        used_memory = memory.percent

        return {
            "Total_Memory" : total_memory,
            "Available_Memory" : available_memory,
            "Used_Memory_%" :used_memory 
        }
    except Exception as e:
            print(f"Error checking memory usage: {e}")
            return None

def check_disk_usage():
    '''
    checks the disk usage of system

    Parameters --> none
    Returns --> Total//used disk, type--> float
    '''
    try:
        disk = psutil.disk_usage('/')

        #to the power 3 converts from bytes to gigabytes
        total_disk = disk.total / (1024**3)
        used_disk = disk.used / (1024**3)


        return {
            "Total_Disk" : total_disk,
            "Used_Disk" : used_disk
        }
    except Exception as e:
            print(f"Error checking disk usage: {e}")
            return None



def create_alerts(cpu_percentage, used_memory, used_disk):
    '''
    checks systems usage and generate alerts if 
    CPU usage exceeds 80%
    Memory usage exceeds 75%
    Disk space usage exceeds 90%
    '''

    if cpu_percentage > 80: 
        print('CPU PERCENTAGE IS HIGH')
    
    if used_memory > 75:
        print('MEMORY USAGE IS HIGH')

    if used_disk > 90:
        print('DISK USAGE IS HIGH')

def generate_report(output_format, interval):
    cpu_percentage = check_cpu_usage_percentage(interval)
    used_memory = check_memory_usage()
    used_disk = check_disk_usage()

    #raise alert
    cpu_percentage = check_cpu_usage_percentage(interval)['CPU_Percentage']
    used_memory = check_memory_usage()['Used_Memory_%']
    used_disk = check_disk_usage()['Used_Disk']

    create_alerts(cpu_percentage, used_memory, used_disk)

    #prepare report data
    report = {
        "CPU_Usage(%)": cpu_percentage,
        "Memory_Usage": used_memory,
        "Disk_Usage" : used_disk
    }

    #Generate report
    if output_format == "text":
        filename = 'system_report.txt'
        with open(filename, "w") as file:
            file.write(f"System Report\n")
            file.write(f"CPU Usage: {cpu_percentage}%\n")
            file.write(f"Memory Usage: {used_memory}\n")
            file.write(f"Disk Usage: {used_disk}\n")
           
    elif output_format == "json":
        filename = 'system_report.json'
        with open(filename, "w") as file:
            json.dump(report, file, indent=4)
    elif output_format == "csv":
        filename = 'system_report.csv'
        with open(filename, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Metric", "Details"])
            writer.writerow(f"CPU Usage: {cpu_percentage}%\n")
            writer.writerow(f"Memory Usage: {used_memory}\n")
            writer.writerow(f"Disk Usage: {used_disk}\n")

    else:
        print("Unsupported format specified.")
        return

    print(f"System report generated: {filename}")

def main():
    parser = argparse.ArgumentParser(description="System Performance Monitoring Script")
    parser.add_argument("--interval", type=int, default=1, help="Monitoring interval in seconds (default: 1)")
    parser.add_argument("--format", type=str, choices=["text", "json", "csv"], default="text", help="Output file format (default: text)")
    args = parser.parse_args()

    generate_report(args.format, args.interval)

if __name__ == "__main__":
    main()
    



