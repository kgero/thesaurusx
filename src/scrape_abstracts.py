
with open('../dat/arxiv/arxivData.json', 'r') as fle_in:
    with open('../dat/arxiv/summaries.txt', 'w') as fle_out:
        for line in fle_in:
            if "\"summary\"" in line:
                summ = line[20:-3]
                fle_out.write(summ)
                fle_out.write('\n\n')
