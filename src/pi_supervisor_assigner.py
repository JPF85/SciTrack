import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# Get the path to the script's directory (src)
base_dir = Path(__file__).resolve().parent

# Go up one level to the parent folder, then into data/members.json
data_path = base_dir.parent / "data" / "members.json"

# Load members
with open(data_path, "r") as f:
    members = json.load(f)

# Filter out members whose memEnd is not None (only active members)
active_members = [m for m in members if m["memEnd"] is None]

# Select 15 random PIs from active members
all_ids = [m["memID"] for m in active_members]
selected_pis = random.sample(all_ids, 15)

# Separate non-PI members from active members
non_pi_ids = [m["memID"] for m in active_members if m["memID"] not in selected_pis]
random.shuffle(non_pi_ids)

# Split into 15 groups with at least 5 each
pi_groups = {pi: [] for pi in selected_pis}

# First give each PI 5 members
for pi in selected_pis:
    for _ in range(5):
        if non_pi_ids:
            pi_groups[pi].append(non_pi_ids.pop())

# Distribute remaining members randomly among PIs
for emp in non_pi_ids:
    chosen_pi = random.choice(selected_pis)
    pi_groups[chosen_pi].append(emp)

# Build PI entries
pi_entries = []
for pi, employees in pi_groups.items():
    for emp in employees:
        pi_entries.append({"empID": emp, "piID": pi})

# look up start date so that no supevisor relationship will have mismatched dates
mem_start_lookup = {m["memID"]: datetime.fromisoformat(m["memStart"]) for m in members}

# Build Supervisor entries with supStart date
supervisor_entries = []
for pi, employees in pi_groups.items():
    
    # make sure employees is not empty
    if not employees:
        continue
    
    # pick 1-5 supervisors from this PI's group
    num_supervisors = min(random.randint(1, 5), len(employees))
    supervisors = random.sample(employees, num_supervisors)
    
    for sup in supervisors:
        # assign 1-5 employees under each supervisor
        possible_subs = [e for e in employees if e != sup]
        num_subs = min(random.randint(1, 5), len(possible_subs))
        subordinates = random.sample(possible_subs, num_subs)
        
        for sub in subordinates:
            mem_start = mem_start_lookup[sub]
            now = datetime.now()
            # Random date between mem_start and now
            delta_days = (now - mem_start).days
            
            if delta_days > 0:
                random_days = random.randint(1, delta_days)
                sup_start = mem_start + timedelta(days=random_days)
            else:
                # If mem_start is today or in future (edge case), just use mem_start
                sup_start = mem_start
            
            supervisor_entries.append({
                "subID": sub,
                "superID": sup,
                "supStart": sup_start.strftime("%Y-%m-%d"),
                "supEnd": None
            })

# randomly add end date for some values
for entry in supervisor_entries:
    
    # 10% chance to add a supEnd
    if random.random() < 0.1:  # 0.1 = 10%
        # parse the supStart back to a datetime
        start_date = datetime.strptime(entry["supStart"], "%Y-%m-%d")
        # choose a random end date after start_date but before now
        days_since_start = (datetime.now() - start_date).days
        
        # only if there's at least 1 day after start
        if days_since_start > 1:  
            random_offset = random.randint(1, days_since_start)
            end_date = start_date + timedelta(days=random_offset)
            entry["supEnd"] = end_date.strftime("%Y-%m-%d")

# output path
timestamp1 = datetime.now().strftime("%Y%m%d_%H%M%S")
pi_output = base_dir.parent / "data" / f"{timestamp1}_pi_table.json"

timestamp2 = datetime.now().strftime("%Y%m%d_%H%M%S")
sup_output = base_dir.parent / "data" / f"{timestamp2}_supervisor_table.json"

# dump files
with open(pi_output, "w") as f:
    json.dump(pi_entries, f, indent=2)
with open(sup_output, "w") as f:
    json.dump(supervisor_entries, f, indent=2)

# print confirmation
print("Generated PI and Supervisor tables with:")
print(f"  PIs: {len(pi_entries)} entries")
print(f"  Supervisors: {len(supervisor_entries)} entries")
