from scipy import stats
import statsmodels.api as sm
import numpy as np

def if_norm(data):
    #シャピロウィルクの検定
    #帰無仮説は「dataが正規分布に従う」
    cert = stats.shapiro(data)
    #qq = sm.qqplot(data, line='r')
    if cert.pvalue > 0.05:
        #帰無仮説は棄却されない
        #dataが正規分布に従う
        return True
    else:
        #帰無仮説は棄却される
        return False

def cert_f(A, B):
    #F検定
    #帰無仮説は「対象の2群の分散に差はない」
    A_var = np.var(A, ddof=1)  # Aの不偏分散
    B_var = np.var(B, ddof=1)  # Bの不偏分散
    A_df = len(A) - 1  # Aの自由度
    B_df = len(B) - 1  # Bの自由度
    bigger_var = np.max([A_var, B_var])
    smaller_var = np.min([A_var, B_var])
    f = smaller_var / bigger_var  # F比の値
    one_sided_pval1 = stats.f.cdf(f, A_df, B_df)  # 片側検定のp値 1
    one_sided_pval2 = stats.f.sf(f, A_df, B_df)   # 片側検定のp値 2
    two_sided_pval = min(one_sided_pval1, one_sided_pval2) * 2  # 両側検定のp値
    print('F:       ', round(f, 3))
    print('p-value: ', round(two_sided_pval, 3))
    print("\n")
    if two_sided_pval > 0.05:
        #帰無仮説は棄却されない
        #等分散性を認める
        return True
    else:
        #帰無仮説は棄却される
        #不等分散性を認める
        return False
    
def cert_t(d1, d2):
    #対応のあるt検定
    #帰無仮説は「2群間の平均値に差がない」
    cert = stats.ttest_rel(d1, d2)
    a1 = np.mean(d1)
    a2 = np.mean(d2)
    if cert.pvalue > 0.05:
        print("2群間の平均値に差があるとはいえない")
        print('T:       ', cert[0])
        print('p-value: ', cert[1])
        print("\n")
        return "average", a1, a2
    else:
        print("2群間の平均値に差があるといえる")
        print('T:       ', cert[0])
        print('p-value: ', cert[1])
        print("\n")
        return "average", a1, a2

def cert_student_t(d1, d2):
    #Studentのt検定
    #帰無仮説は「2群間の平均値に差がない」
    cert = stats.ttest_ind(d1, d2)
    a1 = np.mean(d1)
    a2 = np.mean(d2)
    if cert.pvalue > 0.05:
        print("2群間の平均値に差があるとはいえない")
        print('T:       ', cert[0])
        print('p-value: ', cert[1])
        print("\n")
        return "average", a1, a2
    else:
        print("2群間の平均値に差があるといえる")
        print('T:       ', cert[0])
        print('p-value: ', cert[1])
        print("\n")
        return "average", a1, a2

def cert_welch_t(d1, d2):
    #Welchのt検定
    #帰無仮説は「2群間の平均値に差がない」
    cert = stats.ttest_ind(d1, d2, equal_var=False)
    a1 = np.mean(d1)
    a2 = np.mean(d2)
    if cert.pvalue > 0.05:
        print("2群間の平均値に差があるとはいえない")
        print('T:       ', cert[0])
        print('p-value: ', cert[1])
        print("\n")
        return "average", a1, a2
    else:
        print("2群間の平均値に差があるといえる")
        print('T:       ', cert[0])
        print('p-value: ', cert[1])
        print("\n")
        return "average", a1, a2

def cert_Mann_Whitney_U(d1, d2):
    #Mann-WhitneyのU検定
    #帰無仮説は「独立2群間の代表値に差がない」
    cert = stats.mannwhitneyu(d1, d2, alternative='two-sided')
    if cert.pvalue > 0.05:
        print("2群間の代表値に差があるとはいえない")
    else:
        print("2群間の代表値に差があるといえる")
    return 0

def cert_Wilcoxon(d1, d2):
    #Wilcoxonの符号付順位和検定
    #帰無仮説は「独立2群間の代表値に差がない」
    cert = stats.wilcoxon(d1, d2)
    if cert.pvalue > 0.05:
        print("2群間の代表値に差があるとはいえない")
    else:
        print("2群間の代表値に差があるといえる")
    return 0

def main(d1, d2, c):
    #対応のあるデータか
    if c == 0:
        #対応がある
        if if_norm(d1) and if_norm(d2):
            #2群とも正規性がある
            print("対応のあるデータは正規性があるためt検定を実施\n")
            return cert_t(d1, d2)
        else:
            #正規性が認められない
            print("対応のあるデータに正規性が認められないためWilcoxonの符号順位検定を実施\n")
            return cert_Wilcoxon(d1, d2)
    else:
        #対応がない
        if if_norm(d1) and if_norm(d2):
            #2群とも正規性がある
            if cert_f(d1, d2):
                #等分散性を認める
                print("独立した二つのデータに正規性があり等分散性があるためStudentのt検定を実施\n")
                return cert_student_t(d1, d2)
            else:
                #不等分散性を認める
                print("独立した二つのデータに正規性があり不等分散性があるためWelchのt検定を実施\n")
                return cert_welch_t(d1, d2)
        else:
            #正規性が認められない
            print("独立した二つのデータに正規性が認められないためMann-WhitneyのU検定を実施\n")
            return cert_Mann_Whitney_U(d1, d2)
