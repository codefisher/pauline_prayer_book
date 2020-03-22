//
//  AppNavigationController.swift
//  Pauline Prayer Book
//
//  Created by Michael Buckley on 20/3/20.
//  Copyright © 2020 Michael Buckley. All rights reserved.
//

import Foundation
import UIKit

class AppNavigationController: UINavigationController {

    override func viewDidLoad() {
        super.viewDidLoad()
        self.navigationBar.delegate = self
    }
}

extension AppNavigationController : UINavigationBarDelegate {
    public func navigationBar(_ navigationBar: UINavigationBar, shouldPop item: UINavigationItem) -> Bool {
        if let view = self.visibleViewController as? MenuItemTableViewController {
            if(view.history.count != 0) {
                let historyItem = view.history.popLast()
                if(historyItem != nil) {
                    view.currentMenuitems = (historyItem as? [MenuItem])!
                    view.tableView.reloadData()
                    return false
                }
            }
        }
        return true
    }
}
