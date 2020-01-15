import pymysql
import pymssql


def build_freq_maps(stat_query, target_conn):
    target_conn.cursor()
    [freqmaps, highest_revision, trailing_revision] = build_freqmap(target_conn, stat_query.querysql, stat_query.mostrecentrevision, stat_query.trailingrevisionnumber, stat_query.key_length)
    return [freqmaps, highest_revision, trailing_revision]

def build_freqmap(target_conn, query, most_recent_revision, trailing_revision_number, key_length):
    cur = target_conn.cursor()
    cur.execute(query, (trailing_revision_number,))
    freqmaps = dict()
    freqmap = dict()
    latest_freqmap = dict()
    highest_revision = most_recent_revision
    trailing_revision = trailing_revision_number
    for response in cur:
        if response[0] > highest_revision:
            increment_amount = (int(response[0]) - int(highest_revision))
            highest_revision = int(response[0])
            trailing_revision += increment_amount
        key_response = response[1:len(response)]
        key = ""
        for part_key in range(0, key_length):
            if (part_key == key_length - 1):
                key = key + str(key_response[part_key])
            else:
                key = key + str(key_response[part_key]) + ", "
        if (freqmap.get(key) is None):
            freqmap[key] = dict()

        if (int(response[0]) > most_recent_revision and latest_freqmap.get(key) is None):
            latest_freqmap[key] = dict()

        inner_freq_map = freqmap[key]
        z_value = str(response[key_length+1])
        if inner_freq_map.get(z_value) is None:
            inner_freq_map[z_value] = 1
        else:
            inner_freq_map[z_value] = inner_freq_map.get(z_value) + 1

        if response[0] > most_recent_revision:
            latest_inner_freq_map = latest_freqmap[key]
            z_value = str(response[key_length+1])
            if latest_inner_freq_map.get(z_value) is None:
                latest_inner_freq_map[z_value] = 1
            else:
                latest_inner_freq_map[z_value] = latest_inner_freq_map.get(z_value) + 1
    cur.close()
    freqmaps["freqmap"] = freqmap
    freqmaps["latest_freqmap"] = latest_freqmap
    return [freqmaps, highest_revision, trailing_revision]