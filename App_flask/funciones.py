import pickle

def calcular_ratios(a_circulante, a_circulante3, p_liquido, p_liquido3,total_a,total_a3, total_p,total_p3, r_de_e,r_de_e3, f_p, f_p3, otros_a_liquidos,otros_a_liquidos3, deudores,deudores3, ebitda, ebitda3, c_f, c_f3, tesoreria,tesoreria3): # meter los de 3
    ratio_liquidez = float(a_circulante)/float(p_liquido)
    ratio_de_solvencia_percent = float(total_a) / float(total_p)
    ROE = float(r_de_e)/float(f_p)
    deuda_neta = float(total_p) - (float(otros_a_liquidos)+float(deudores)) #quitar deuda neta del form
    net_debt_ebitda = float(deuda_neta)/float(ebitda)
    ratio_endeudamiento = float(total_p)/float(f_p)

    ratio_liquidez3 = float(a_circulante3)/float(p_liquido3)
    ratio_de_solvencia_percent3 = float(total_a3) / float(total_p3)
    ROE3 = float(r_de_e3)/float(f_p3)
    deuda_neta3 = float(total_p3) - (float(otros_a_liquidos3)+float(deudores3)) #quitar deuda neta del form
    net_debt_ebitda3 = float(deuda_neta3)/float(ebitda3)
    ratio_endeudamiento3 = float(total_p3)/float(f_p3)

    ratio_liquidez_cambio = ((ratio_liquidez-ratio_liquidez3)/ratio_liquidez3)*100
    ratio_de_solvencia_percent_cambio = ((ratio_de_solvencia_percent-ratio_de_solvencia_percent3)/ratio_de_solvencia_percent3)*100
    ROE_cambio = ((ROE-ROE3)/ROE3)*100
    deuda_neta_cambio = ((deuda_neta-deuda_neta3)/deuda_neta3)*100
    net_debt_ebitda_cambio = ((net_debt_ebitda-net_debt_ebitda3)/net_debt_ebitda3)*100
    ratio_endeudamiento_cambio = ((ratio_endeudamiento-ratio_endeudamiento3)/ratio_endeudamiento3)*100
    c_f_cambio =  ((float(c_f) - float(c_f3))/float(c_f3))*100
    tesoreria_cambio = ((float(tesoreria) - float(tesoreria3))/float(tesoreria3))*100

    return  ratio_endeudamiento_cambio, ratio_endeudamiento, ratio_liquidez_cambio, ratio_liquidez, net_debt_ebitda_cambio, net_debt_ebitda, deuda_neta_cambio, deuda_neta,ROE_cambio, ROE, ratio_de_solvencia_percent_cambio, ratio_de_solvencia_percent, c_f_cambio, c_f, tesoreria_cambio, tesoreria 
  

def calcular_ratios_log(a_circulante, a_circulante3, p_liquido, p_liquido3,total_a,total_a3, total_p,total_p3, r_de_e,r_de_e3, f_p, f_p3, otros_a_liquidos,otros_a_liquidos3, deudores,deudores3, ebitda, ebitda3):
    ratio_liquidez = float(a_circulante)/float(p_liquido)
    ratio_de_solvencia_percent = float(total_a) / float(total_p)
    ROE = float(r_de_e)/float(f_p)
    deuda_neta = float(total_p) - (float(otros_a_liquidos)+float(deudores)) #quitar deuda neta del form
    net_debt_ebitda = float(deuda_neta)/float(ebitda)
    ratio_endeudamiento = float(total_p)/float(f_p)

    ratio_liquidez3 = float(a_circulante3)/float(p_liquido3)
    ratio_de_solvencia_percent3 = float(total_a3) / float(total_p3)
    ROE3 = float(r_de_e3)/float(f_p3)
    deuda_neta3 = float(total_p3) - (float(otros_a_liquidos3)+float(deudores3)) #quitar deuda neta del form
    net_debt_ebitda3 = float(deuda_neta3)/float(ebitda3)
    ratio_endeudamiento3 = float(total_p3)/float(f_p3)

    ratio_liquidez_cambio = ((ratio_liquidez-ratio_liquidez3)/ratio_liquidez3)*100
    ratio_de_solvencia_percent_cambio = ((ratio_de_solvencia_percent-ratio_de_solvencia_percent3)/ratio_de_solvencia_percent3)*100
    ROE_cambio = ((ROE-ROE3)/ROE3)*100
    deuda_neta_cambio = ((deuda_neta-deuda_neta3)/deuda_neta3)*100
    net_debt_ebitda_cambio = ((net_debt_ebitda-net_debt_ebitda3)/net_debt_ebitda3)*100
    ratio_endeudamiento_cambio = ((ratio_endeudamiento-ratio_endeudamiento3)/ratio_endeudamiento3)*100

    return  ratio_endeudamiento_cambio, ratio_endeudamiento, ratio_liquidez_cambio, ratio_liquidez, net_debt_ebitda_cambio, net_debt_ebitda, deuda_neta_cambio, deuda_neta,ROE_cambio, ROE, ratio_de_solvencia_percent_cambio, ratio_de_solvencia_percent
  


