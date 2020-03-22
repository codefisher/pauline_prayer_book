//
//  AppDelegate.swift
//  Pauline Prayer Book
//
//  Created by Eremita on 25/04/17.
//
//

import UIKit

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?

    override func buildMenu(with builder: UIMenuBuilder) {
        guard builder.system == .main else { return }
        builder.remove(menu: .format)
        
        let printSelector = #selector(ViewController.printPage)
        let printPage = UIKeyCommand(
          title: NSLocalizedString("Print", comment: ""),
          image: nil,
          action: printSelector,
          input: "p",
          modifierFlags: [.command],
          propertyList: nil)
        
        let menuPrint = UIMenu(
          title: "",
          image: nil,
          identifier: nil,
          options: .displayInline,
          children: [printPage])
        
        builder.insertChild(menuPrint, atStartOfMenu: .file)
        
        let aboutSelector = #selector(ViewController.openAbout)
        let openAbout = UIKeyCommand(
          title: NSLocalizedString("About", comment: ""),
          image: nil,
          action: aboutSelector,
          input: "a",
          modifierFlags: [.command],
          propertyList: nil)
        
        let menuAbout = UIMenu(
          title: "",
          image: nil,
          identifier: nil,
          options: .displayInline,
          children: [openAbout])
        
        builder.insertChild(menuAbout, atEndOfMenu: .help)
        
        let settingSelector = #selector(ViewController.goSettings)
        let goSettings = UIKeyCommand(
          title: NSLocalizedString("Settings", comment: ""),
          image: nil,
          action: settingSelector,
          input: "s",
          modifierFlags: [.command],
          propertyList: nil)
        
        let menuSettings = UIMenu(
          title: "",
          image: nil,
          identifier: nil,
          options: .displayInline,
          children: [goSettings])
        
        builder.insertChild(menuSettings, atStartOfMenu: .file)
        
    }

    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey : Any]? = nil) -> Bool {
        // Override point for customization after application launch.
        return true
    }

    func applicationWillResignActive(_ application: UIApplication) {
        // Sent when the application is about to move from active to inactive state. This can occur for certain types of temporary interruptions (such as an incoming phone call or SMS message) or when the user quits the application and it begins the transition to the background state.
        // Use this method to pause ongoing tasks, disable timers, and throttle down OpenGL ES frame rates. Games should use this method to pause the game.
    }

    func applicationDidEnterBackground(_ application: UIApplication) {
        // Use this method to release shared resources, save user data, invalidate timers, and store enough application state information to restore your application to its current state in case it is terminated later.
        // If your application supports background execution, this method is called instead of applicationWillTerminate: when the user quits.
    }

    func applicationWillEnterForeground(_ application: UIApplication) {
        // Called as part of the transition from the background to the inactive state; here you can undo many of the changes made on entering the background.
    }

    func applicationDidBecomeActive(_ application: UIApplication) {
        // Restart any tasks that were paused (or not yet started) while the application was inactive. If the application was previously in the background, optionally refresh the user interface.
    }

    func applicationWillTerminate(_ application: UIApplication) {
        // Called when the application is about to terminate. Save data if appropriate. See also applicationDidEnterBackground:.
    }


}

