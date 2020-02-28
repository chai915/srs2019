import csv
with open("/Users/chloe/Desktop/SRS Project/editedQueries.txt", "r") as data_file:

    lines_list = data_file.readlines()

    #label = abruzzo
    #starting with | is a query

    current_label = "Placeholder"

    label_list = []
    query_list = []

    for line in lines_list:
        #label name
        if line[0] != '|':
            current_label = line.strip()

        elif line[0] == "|":
            start_val = line.find('"')
            end_val = line.rfind('"')

            query = line[int(start_val + 1):int(end_val)]

            label_list.append(current_label)
            query_list.append(query)

    with open('/Users/chloe/Desktop/SRS Project/query_file.csv', 'w', newline='') as myfile:
        writer = csv.writer(myfile)
        writer.writerow(["Label", "Query"])
        for x in range(0, len(label_list)):
            writer.writerow([label_list[x], query_list[x]])

    





