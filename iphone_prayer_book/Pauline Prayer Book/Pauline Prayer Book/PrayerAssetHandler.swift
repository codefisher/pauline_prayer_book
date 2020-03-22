
//
//  PrayerWebView.swift
//  Pauline Prayer Book
//
//  Created by Michael Buckley on 22/2/20.
//  Copyright © 2020 Michael Buckley. All rights reserved.
//

import Foundation
import WebKit
import MobileCoreServices

class PrayerAssetHandler: NSObject, WKURLSchemeHandler {
    
    func webView(_ webView: WKWebView, start urlSchemeTask: WKURLSchemeTask) {
        let url = urlSchemeTask.request.url!
        
        let pathArr = url.path.components(separatedBy: ".")
        let forResource: String = pathArr[0]
        let ofType: String? = pathArr.count > 1 ? pathArr[1] : nil
        
        let bundlePath = Bundle.main.path(forResource: "prayers" + forResource, ofType: ofType)
        if(bundlePath == nil) {
            return
        }
        
        let fileExtension: CFString = ofType! as CFString
        guard
            let extUTI = UTTypeCreatePreferredIdentifierForTag(kUTTagClassFilenameExtension,
                                fileExtension, nil)?.takeUnretainedValue()
        else { return }

        guard
            let mimeUTI: NSString = UTTypeCopyPreferredTagWithClass(extUTI,
                                kUTTagClassMIMEType)?.takeRetainedValue()
        else { return }
        
        let mimeType: String = mimeUTI as String
        
        do {
            let data: Data = try NSData(contentsOfFile: bundlePath!) as Data
        
            //Create a NSURLResponse with the correct mimetype.
            let urlResponse = URLResponse(url: url, mimeType: mimeType,
                                          expectedContentLength: data.count, textEncodingName: "utf8")
            urlSchemeTask.didReceive(urlResponse)
            urlSchemeTask.didReceive(data)
            urlSchemeTask.didFinish()
        }  catch _ as NSError {
            return
        }
        
    }
    
    func webView(_ webView: WKWebView, stop urlSchemeTask: WKURLSchemeTask) {
    }
}
