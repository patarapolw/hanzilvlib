if __name__ == '__main__':
    with open('hanzi_dict.csv') as fin, open('hanzi_dict0.csv', 'w') as fout:
        for i, row in enumerate(fin):
            if i == 0:
                row = row.lower()

            fout.write(row)
