import re
import string


def cond(name):
    return (len(name) > 1 and
            name[0] not in "'-" and
            name[-1] not in "'-" and
            not re.search(r"['-]{2,}", name))


students = []
# pop = distinct students, activity = # of submissions, difficulty = score
popularity, activity, scores = [set() for e in range(4)], [0] * 4, []
courses = [(0, 'Python', 600), (1, 'DSA', 400), (2, 'Databases', 480), (3, 'Flask', 550)]
mail_idx = []
notified = set()
print("Learning progress tracker")
while True:
    cmd = input()
    match cmd:
        case 'exit':
            print('Bye!')
            break
        case x if x in string.whitespace:
            print('No input')
        case 'add students':
            print("Enter student credentials or 'back' to return:")

            while True:
                creds = input()
                if creds == 'back':
                    print(f'Total {len(students)} students have been added.')
                    break

                try:
                    first, rest = creds.split(' ', 1)
                    last, email = rest.rsplit(' ', 1)
                except ValueError:
                    print('Incorrect credentials.')
                    continue
                if email in [line['email'] for line in students]:
                    print('This email is already taken.')
                    continue

                valid = string.ascii_letters + "'-"
                if all(c in valid for c in first) and cond(first):
                    if all(c in valid + ' ' for c in last) and cond(last):
                        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                            line = {
                                "first": first,
                                "last": last,
                                "email": email,
                                "id": str(hash(email) % 100000),
                                "grades": [0, 0, 0, 0]
                            }
                            students.append(line)
                            print('The student has been added.')
                        else:
                            print('Incorrect email.')
                    else:
                        print('Incorrect last name.')
                else:
                    print('Incorrect first name.')
        case 'list':
            if len(students) == 0:
                print('No students found.')
                continue
            print('Students:')
            for student in students:
                print(f'{student["id"]}')
                # print(f'{student["id"]} {" ".join(map(str, student["grades"]))}')

        case 'add points':
            print("Enter an id and points or 'back' to return:")
            while True:
                line = input()
                if line == 'back':
                    break
                edit_id, *grades = line.split()
                valid = [i for i, e in enumerate(students) if e['id'] == edit_id]
                if len(valid) == 0:
                    print(f'No student is found for id={edit_id}.')
                    continue
                idx = valid[0]
                if len(grades) != 4:
                    print('Incorrect points format.')
                    continue
                try:
                    grades = list(map(int, grades))
                except ValueError:
                    print('Incorrect points format.')
                    continue
                if any(g < 0 for g in grades):
                    print('Incorrect grades format.')
                    continue
                # pop = distinct students, activity = # of submissions, difficulty = score
                s = students[idx]
                for i, prev in enumerate(s['grades']):
                    if grades[i] != 0:
                        popularity[i].add(s['id'])
                        activity[i] += 1
                students[idx]['grades'] = [g1 + g2 for g1, g2 in zip(grades, students[idx]['grades'])]
                for i, course_string, max_score in courses:
                    if students[idx]['grades'][i] == max_score and (idx, i) not in notified:
                        mail_idx.append((idx, i))
                print("Points updated.")
        case 'find':
            print("Enter an id or 'back' to return:")
            while True:
                line = input()
                if line == 'back':
                    break
                valid = [i for i, e in enumerate(students) if e['id'] == line]
                if len(valid) == 0:
                    print(f'No student is found for id={line}.')
                    continue
                idx = valid[0]
                s_id, g = students[idx]['id'], students[idx]['grades']
                print('%s points: Python=%d; DSA=%d; Databases=%d; Flask=%d' %
                      (s_id, g[0], g[1], g[2], g[3]))
        case 'statistics':
            print("Type the name of a course to see details or 'back' to quit:")
            course_sizes = [len(c) for c in popularity]
            max_size = max(course_sizes)
            min_size = min(course_sizes)
            most_popular_indexes = [i for i, size in enumerate(course_sizes) if size == max_size]
            least_popular_indexes = [i for i, size in enumerate(course_sizes) if size == min_size]

            most_popular_courses = [courses[i][1] for i in most_popular_indexes]
            if max_size != 0:
                most_popular = f"Most popular: {', '.join(most_popular_courses)}"
            else:
                most_popular = 'Most popular: n/a'

            least_popular_courses = [courses[i][1] for i in least_popular_indexes]
            if most_popular_indexes == least_popular_indexes:
                least_popular = 'Least popular: n/a'
            else:
                least_popular = f"Least popular: {', '.join(least_popular_courses)}"

            max_activity = max(activity)
            min_activity = min(activity)
            most_activity_indexes = [i for i, a in enumerate(activity) if a == max_activity]
            least_activity_indexes = [i for i, a in enumerate(activity) if a == min_activity]

            most_activity_courses = [courses[i][1] for i in most_activity_indexes]
            if max_activity != 0:
                most_activity = f"Highest activity: {', '.join(most_activity_courses)}"
            else:
                most_activity = 'Highest activity: n/a'

            least_activity_courses = [courses[i][1] for i in least_activity_indexes]
            if most_activity_indexes == least_activity_indexes:
                least_activity = 'Lowest activity: n/a'
            else:
                least_activity = f"Lowest activity: {', '.join(least_activity_courses)}"

            py = []
            ds = []
            db = []
            fl = []

            sums = [0, 0, 0, 0]

            for s in students:
                for i, c in enumerate([py, ds, db, fl]):
                    if s['id'] in popularity[i]:
                        sums[i] += s['grades'][i]
                        c.append((s['id'], s['grades'][i], round(s['grades'][i] / courses[i][2], 3) * 100))

            scores = []
            for score, size in zip(sums, course_sizes):
                if size == 0:
                    scores.append(0)
                else:
                    scores.append(score/size)

            max_score = max(scores)
            min_score = min(scores)
            most_score_indexes = [i for i, s in enumerate(scores) if s == max_score]
            least_score_indexes = [i for i, s in enumerate(scores) if s == min_score]

            most_score_courses = [courses[i][1] for i in most_score_indexes]
            if max_score != 0:
                most_score = f"Easiest course: {', '.join(most_score_courses)}"
            else:
                most_score = 'Easiest course: n/a'
            least_score_courses = [courses[i][1] for i in least_score_indexes]
            if max_score == min_score:
                least_score = 'Hardest course: n/a'
            else:
                least_score = f"Hardest course: {', '.join(least_score_courses)}"

            print(most_popular)
            print(least_popular)
            print(most_activity)
            print(least_activity)
            print(most_score)
            print(least_score)

            while True:
                line = input()
                match line.lower():
                    case 'python':
                        course = sorted(py, key=lambda x: x[1], reverse=True)
                        title = courses[0][1]
                    case 'dsa':
                        course = sorted(ds, key=lambda x: x[1], reverse=True)
                        title = courses[1][1]
                    case 'databases':
                        course = sorted(db, key=lambda x: x[1], reverse=True)
                        title = courses[2][1]
                    case 'flask':
                        course = sorted(fl, key=lambda x: x[1], reverse=True)
                        title = courses[3][1]
                    case 'back':
                        break
                    case _:
                        print('Unknown course')
                        continue
                print(title)
                print(f"{'id':<6} {'points':<8} {'completed':<9}")
                for c in course:
                    print(f'{c[0]:<6} {c[1]:<8} {c[2]:<.1f}%')
        case 'notify':
            notif_ppl = set()
            # if stuck on test #32 , there is the possibility where score is the same but
            # id isn't ordered (and we aren't asked to order id) but the test does depend
            # on id ordering causing the test to fail saying ordering is wrong at random.
            for idx, c in mail_idx:
                notif_ppl.add(idx)
                print(f"To: {students[idx]['email']}")
                print(f"Re: Your Learning Progress")
                print(f"Hello, {students[idx]['first']} {students[idx]['last']}! You have accomplished our {courses[c][1]} course!")
            print(f'Total {len(notif_ppl)} students have been notified.')
            notified.update(mail_idx)
            mail_idx = []
        case 'back':
            print("Enter 'exit' to exit the program")
        case _:
            print('Unknown command!')
