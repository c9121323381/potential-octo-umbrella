#!/usr/bin/env python3
# -*- 編碼：utf-8 -*-
"""
最後更新：2018 年 4 月 30 日
該庫包含用於 ECG 信號處理的通用函數。它是
開髮用於描繪來自 STAFFIII 的信號
數據庫（https://physionet.org/physiobank/database/staffiii/）。
delineateMultiLeadECG() 需要 WTdelineator.py 庫。
detectionVoteFusion() 函數中使用的融合技術的詳細信息
可參見：《Data fusion for QRS complex detection in multi-lead
Ledezma 等人 (2015) 的心電圖記錄”。
該庫中包含的所有功能都是在 Multiscale 中開發的
倫敦大學學院 (MUSE-UCL) 心血管工程組
卡洛斯·萊德茲馬。
本作品受知識共享署名-相同方式共享 4.0 保護
國際許可 (https://creativecommons.org/licenses/by-sa/4.0/)
"""

 將numpy 導入為 np

def  augmentedLimbs ( DI , DII ):
    '''
    aVR, aVL, aVF = augmentedLimbs(DI,DII)
    
    使用導聯 DI 和 DII 計算 ECG 增強肢體導聯。
    
    輸入：
        DI（numpy 數組）：包含 DI 引導。
        
        DII（numpy 數組）：包含 DII 導數。
        
    輸出：
        aVR（numpy 數組）：包含計算為：
            aVR = -1/2 * (DI + DII)
        
        aVL（numpy 數組）：包含計算為：
            aVL = DI - 1/2 * DII
            
        aVF（numpy 數組）：包含計算為的 aVF 導聯：
            aVF = -1/2 * DI + DII
    '''
    VR  =  np。至少_2d ( - 1 / 2  * ( DI  +  DII ))。噸
    aVL  =  np。至少 2d ( DI  -  1 / 2  *  DII )。噸
    aVF  =  np。至少_2d ( - 1 / 2  *  DI  +  DII )。噸
    
    返回 aVR , aVL , aVF

def  detectionVoteFusion ( det , win ):
    '''
    detFusion = detectionVoteFusion(det,win)
    
    使用提供的檢測執行投票融合。為了這個工作
    檢測窗口必須與提供的檢測一致。這個
    意味著如果檢測是樣本數，則窗口必須是
    以樣本數給出。或者，如果樣本在
    秒，窗口必須以秒為單位給出。等等...
    
    對於每個檢測矢量（ECG 導聯），該函數比較每個檢測
    與在其他檢測向量中發現的那些。如果至少有一半
    引線包含接近被分析的檢測（由
    窗口），然後驗證檢測。
    
    輸入：
        det（列表）：包含對不同導聯進行的檢測。每個
        lead 必須作為列表提供，其中每個條目都是一個檢測標記。
        
        win（float）：定義不同導聯中兩個檢測何時的窗口
        被認為是相同的。此輸入必須與值一致
        在檢測向量中給出
        
    輸出：
        detFusion(list)：這個變量中的每個列表對應一個列表
        在細節中提供。detFusion 中提供的標記僅是那些
        對每條線索進行了驗證。
    '''
    
    # 初始化解決方案列表
    detFusion  = []
    
    for  lead  in  det : # 一次驗證一個線索
        detFusion  += [[]] # 為當前潛在客戶創建一個新列表
        
        如果 len ( lead ) >  0 :
            for  cand  in  lead : # 遍歷 lead 中的所有檢測
                vote  =  0  # 為每個候選人初始化投票變量
                for  comp  in  det : # 與所有線索進行比較
                    # 如果檢測出現在另一條導聯中則發出信號
                    如果 len ( comp ) >  0 :
                        如果 np。min ( np . abs ( np . array ( comp ) -  cand )) <  win :
                            投票 +=  1
                                
                # 如果在超過一半的通道中確認檢測
                # 索引保存為線索中的確認檢測
                如果 vote / len ( det ) >=  0.5：
                    detFusion [ - 1 ] += [ cand ]

    返回 detFusion

def  delineateMultiLeadECG ( sig , fs ):
    '''
    ECGdelin = delineateMultiLeadECG(sig,fs)
    
    使用 WT 變換和檢測融合描繪多導聯心電圖。這個
    函數需要 WTdelineator 庫。
    
    該算法使用小波對每個導聯執行 QRS 檢測
    轉換。然後，它對標記進行數據融合以僅保留
    可靠的節拍檢測。最後，基於小波的描述
    過程繼續僅使用經過驗證的 R 峰值標記。
    
    輸入：
        sig（numpy 數組）：包含所有要分析的 ECG 導聯。每個
        假設數組的列是一個線索，每一行都是一個樣本。
        
        fs（浮點數）：採集 ECG 時的採樣頻率，以 Hz 為單位。
        
    輸出：
        ECGdelin（列表）：ECG 刪除結果。每一項都是劃定
        ECG 導聯的結果（numpy 數組），對應於那些
        信號中提供。一個圈定結果的每一行對應一個
        找到並驗證了節拍，它的形式是：
            
            ECGdelin[k][i,:] = [Pon, P, Pend, QRSon, R, QRSend, Ton, T, Tend]    
    '''
    
     將WTdelineator 導入為 wt
    
    # WT 變換一次只能使用 2**16 個樣本：
    乞求 =  0
    結束 =  2 ** 16
    最後 = 假
    
    # 初始化將包含結果的列表
    ECGdelin  = []
    
    對於 範圍內的i  ( sig . shape [ 1 ]): 
        ECGdelin  += [ np . 零(( 1 , 9 ), dtype = int )]
    
    while  not  last : # 繼續描繪直到信號結束
        # 初始化臨時數組
        R  = []
        QRSon  = []
        QRSend  = []
        n  = []
        TP  = []
        噸 = []
        趨向 = []
        PP  = []
        龐 = []
        掛起 = []
        
        # 如果在最後一次迭代中到達了信號的末尾，則信號
        # 正在處理最後一段。
        如果 結束 >= 信號。形狀[ 0 ]:
            結束 = 簽名。形狀[ 0 ]
            最後 = 真
            
        # 定義 WT 過濾器
        thisSig  =  sig [求：結束，:]
        N  = 這個簽名。shape [ 0 ] # 信號中的樣本數
        WTfilters  = 重量。waveletFilters ( N , fs ) # 創建過濾器以應用算法
        w  = []
        
        for  lead  in  range ( sig . shape [ 1 ]): # 在每個導聯中找到 QRS 複合波
            w  += [重量。waveletDecomp ( thisSig [:, lead ], WTfilters )] # 保存每個lead的分解
            Rb , nb  = 重量。Rdetection ( w [ - 1 ], fs )
            R  += [ Rb ]
            n  += [ nb ]
        
        # 執行融合以僅保留有效的 QRS 複合波
        win  =  int ( np . floor (( 40 / 1000 ) *  fs ))
        R  =  detectionVoteFusion ( R , win )
        
        # 用可靠的節拍完成勾畫
        對於 範圍內的鉛 （len（R））：             
            _ , _ , Onb , Endb  =  wt。QRSdelineation（R [導聯]，w [導聯]，n [導聯]，fs）
            T1、T2、TonB、TendB  =  wt。Tdelineation ( Endb , w [ lead ], fs ) # 檢測並描繪T波
            P1、P2、PonB、PendB  =  wt。Pdelineation ( Onb , w [ lead ], fs ) # 檢測並描繪P波
            
            # 只保留最大的 T 波峰
            TpB  = []
            對於 枚舉中的idx和Tcand  ( T1 )： 
                如果 Tcand  !=  0：
                    如果( np . abs ( thisSig [ Tcand , lead ]) >  np . abs ( thisSig [ T2 [ idx ], lead ]))或( T2 [ idx ] ==  0 ):
                        TpB  += [ Tcand ]
                    其他：
                        TpB  += [ T2 [ idx ]]
                其他：
                    TpB  += [ Tcand ]
                    
            # 只保留最大的P波峰
            PpB  = []
            對於 idx，枚舉中的Pcand  ( P1 )： 
                如果 Pcand  !=  0：
                    如果( np . abs ( thisSig [ Pcand , lead ]) >  np . abs ( thisSig [ P2 [ idx ], lead ]))或( P2 [ idx ] ==  0 ):
                        PpB  += [ Pcand ]
                    其他：
                        PpB  += [ P2 [ idx ]]
                其他：
                    PpB  += [ Tcand ]
            
            # 保存這個線索的檢測
            QRSon  += [ Onb ]
            QRSend  += [結束]
            Tp  += [ TpB ]
            噸 += [噸 B ]
            傾向 += [ TendB ]
            Pp  += [ PpB ]
            Pon  += [ PonB ]
            掛起 += [ PendB ]
        
        # 將所有內容轉換為 numpy 數組並將結果附加到
        # 變量結束
        對於 範圍內的i  ( sig . shape [ 1 ]): 
            QRSonB  =  np。數組( QRSon [ i ], ndmin = 2 , dtype = int )
            QRSonB  += 請求 * ( QRSonB > 0 )
            
            Rb  =  np。數組( R [ i ], ndmin = 2 , dtype = int )
            Rb  +=  beg  * ( Rb > 0 )
            
            QRSendB  =  np。數組( QRSend [ i ], ndmin = 2 , dtype = int )
            QRSendB  += 請求 * ( QRSendB > 0 )
            
            TpB  =  np。數組( Tp [ i ], ndmin = 2 , dtype = int )
            TpB  += 求 * ( TpB > 0 )
            
            TonB  =  np。array ( Ton [ i ], ndmin = 2 , dtype = int )
            TonB  += 乞求 * ( TonB > 0 )
            
            趨勢 B  =  np。array (趨向[ i ], ndmin = 2 , dtype = int )
            TendB  +=  beg  * ( TendB > 0 )
            
            PpB  =  np。數組( Pp [ i ], ndmin = 2 , dtype = int )
            PpB  += 乞求 * ( PpB > 0 )
            
            PonB  =  np。數組( Pon [ i ], ndmin = 2 , dtype = int )
            PonB  += 乞求 * ( PonB > 0 )
            
            PendB  =  np。數組( Pend [ i ], ndmin = 2 , dtype = int )
            PendB  +=  beg  * ( PendB > 0 )
            
            ECGdelinB  =  np . 連接(( PonB , PpB , PendB ,\
                                        QRSonB , Rb , QRSendB ,\
                                        TonB，TpB，TendB），軸= 0）。噸
            ECGdelin [ i ] =  np。連接(( ECGdelin [ i ], ECGdelinB ), axis = 0 )
        
        求 = 結束
        結束 +=  2 ** 16
        
    for  i  in  range ( sig . shape [ 1 ]): # 刪除初始化行
        ECGdelin [ i ] =  np。刪除( ECGdelin [ i ], 0 , axis = 0 )
        
    返回 ECGdelin
