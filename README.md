# potential-octo-umbrella

WT輪廓標
在 python 中實現的基於小波的 ECG 描繪器庫

在 WTdelineator.py 中提供了執行 ECG 描繪所需的庫以及使用說明。此實現基於以下工作：Martínez、Juan Pablo 等人。“基於小波的 ECG 描繪器：對標準數據庫的評估。” IEEE 生物醫學工程彙刊 51.4 (2004)：570-581。

提供了兩個示例，一個對 STAFFIII 數據庫 ( https://physionet.org/physiobank/database/staffiii/ )的單個信號 (delineateSignal.py) 進行描繪，另一個對整個數據庫 (delineateDatabase.py) 進行描繪。它們都需要 pyhon PhysioToolkit WFDB python 包 ( https://github.com/MIT-LCP/wfdb-python )。第二個示例需要 annotations.csv 文件，它是 STAFFIII 文件中提供的註釋的匯總版本。

此存儲庫中包含的所有功能均由 Carlos Ledezma 在倫敦大學學院 (MUSE-UCL) 的多尺度心血管工程小組開發。

本作品受知識共享署名-相同方式共享 4.0 國際許可 ( https://creativecommons.org/licenses/by-sa/4.0/ )保護
參考:https://github.com/caledezma/WTdelineator
