def GMM_get_weights_given_input(I, NUM_COMPONENTS, global_weights, global_means, global_cov, INPUT_DIM, OUTPUT_DIM):

    weights_given_i_array = np.zeros(NUM_COMPONENTS)
    pdf_list = []
    pdf_weights_total = 0.0

    for k in range(NUM_COMPONENTS):
        mu_i = global_means[k, :INPUT_DIM]
        sigma_i = global_cov[k, :INPUT_DIM, :INPUT_DIM]
        pdf_i = multivariate_normal.pdf(I, mu_i, sigma_i)
        pdf_list.append(pdf_i)
        pdf_weights_total += global_weights[k] * pdf_i

    for j in range(NUM_COMPONENTS):
        weights_given_i_array[j] = global_weights[j] * pdf_list[j] / pdf_weights_total

    return weights_given_i_array


def GMM_get_means_given_input(I, NUM_COMPONENTS, means, cov, INPUT_DIM, OUTPUT_DIM):

    mu_o_given_i_array = np.zeros((NUM_COMPONENTS, OUTPUT_DIM))
    mu_o_given_i_total = np.zeros(OUTPUT_DIM)

    for k in range(NUM_COMPONENTS):
        mu_o = means[k, INPUT_DIM:]
        mu_i = means[k, :INPUT_DIM]
        sigma_oi = cov[k, INPUT_DIM:, :INPUT_DIM]
        sigma_i_inverse = np.linalg.inv(cov[k, :INPUT_DIM, :INPUT_DIM])
        mu_o_given_i = mu_o + sigma_oi.dot(sigma_i_inverse).dot(I - mu_i)
        mu_o_given_i_array[k, :] = mu_o_given_i

    return mu_o_given_i_array


def GMM_get_cov_given_input(I, NUM_COMPONENTS, means, cov, INPUT_DIM, OUTPUT_DIM):

    sigma_o_given_i_array = np.zeros((NUM_COMPONENTS, OUTPUT_DIM, OUTPUT_DIM))
    sigma_o_given_i_total = np.zeros((OUTPUT_DIM, OUTPUT_DIM))

    for k in range(NUM_COMPONENTS):
        sigma_o = cov[k, INPUT_DIM:, INPUT_DIM:]
        sigma_oi = cov[k, INPUT_DIM:, :INPUT_DIM]
        sigma_i_inverse = np.linalg.inv(cov[k, :INPUT_DIM, :INPUT_DIM])
        sigma_io = cov[k, :INPUT_DIM, INPUT_DIM:]
        sigma_o_given_i = sigma_o - sigma_oi.dot(sigma_i_inverse).dot(sigma_io)
        sigma_o_given_i_array[k, :, :] = sigma_o_given_i

    return sigma_o_given_i_array

