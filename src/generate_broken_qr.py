import qr


def generate_broken_qr(message, ecc, version, mask, filename):
    q0 = qr.generate_qr_code(message, ecc, version, mask)
    qr_matrix = qr.qr_matrix(q0)
    broken_qr_matrix = cover_format_modules(qr_matrix)
    output_path = 'demo/' + filename + '.png'
    qr.qr_matrix_image(broken_qr_matrix, output_path, show=False)
    return output_path


def cover_format_modules(qr_matrix):
    """
    Takes in numpy matrix of qr_matrix and changes any 0s in the format
    specification areas to 1s
    """
    for i in range(8):
        qr_matrix[8][i] = 1 # horizontal top left
        qr_matrix[8][-i] = 1 # horizontal top right
        qr_matrix[i][8] = 1 # vertical top left
        qr_matrix[-i][8] = 1 # vertical bottom left
    return qr_matrix

# if __name__ == '__main__':
#     generate_broken_qr('./tests/target/yahoo.png')
