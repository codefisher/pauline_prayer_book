//
//  menuViewController.swift
//  Pauline Prayer Book
//
//  Created by Eremita on 27/04/17.
//
//

import UIKit

class MenuViewController: UIViewController, UIPickerViewDelegate, UIPickerViewDataSource {

    @IBOutlet weak var prayerLanguage: UIPickerView!
    var languageData: [String] = [String]()
    var languageValues: [String] = [String]()
    
    @IBOutlet weak var fontSize: UIPickerView!
    var fontSizeData: [String] = [String]()
    var fontSizeValue: [String] = [String]()
    
    var languageChange = false
    
    @IBOutlet weak var theme: UISegmentedControl!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        let defaults = UserDefaults.standard // standardUserDefaults()
        
        // Connect data:
        self.prayerLanguage.delegate = self
        self.prayerLanguage.dataSource = self
        
        self.fontSize.delegate = self
        self.fontSize.dataSource = self
        
        // Do any additional setup after loading the view.
        languageData = [NSLocalizedString("English", comment: ""),
                        NSLocalizedString("Polish", comment: ""),
                        NSLocalizedString("Latin", comment: ""),
                        NSLocalizedString("Italian", comment: ""),
                        NSLocalizedString("German", comment: ""),
                        NSLocalizedString("Croation", comment: ""),
                        NSLocalizedString("Slovak", comment: "")]
        languageValues = ["en", "pl", "la", "it", "de", "hr", "sk"]
        
        var language = defaults.string(forKey: "prayer_language")
        if language == nil {
            language = NSLocalizedString("default_locale", comment: "")
        }
        
        let activeLanguage = languageValues.firstIndex(of: language!)
        if activeLanguage != nil {
            self.prayerLanguage.selectRow(activeLanguage!, inComponent: 0, animated: false)
        }
        
        fontSizeData = ["8", "11", "14", "17", "20", "24", "28", "32", "36", "48"]
        fontSizeValue = ["8", "11", "14", "17", "20", "24", "28", "32", "36", "48"]
 
        var fontSize = defaults.string(forKey: "font_size")
        if fontSize == nil {
            fontSize = "14"
        }
        
        let activeFontSize = fontSizeValue.firstIndex(of: fontSize!)
        if activeFontSize != nil {
            self.fontSize.selectRow(activeFontSize!, inComponent: 0, animated: false)
        }
        
        let currentTheme = defaults.integer(forKey: "theme_type")
        theme.selectedSegmentIndex = currentTheme
        
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    // The number of columns of data
    func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 1
    }
    
    // The number of rows of data
    func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        if pickerView == self.prayerLanguage {
            return languageData.count
        } else {
            return fontSizeData.count
        }
        
    }
    
    // The data to return for the row and component (column) that's being passed in
    func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        if pickerView == self.prayerLanguage {
            return languageData[row]
        } else {
            return fontSizeData[row]
        }
    }
    
    // Catpure the picker view selection
    func pickerView(_ pickerView: UIPickerView, didSelectRow row: Int, inComponent component: Int) {
        // This method is triggered whenever the user makes a change to the picker selection.
        // The parameter named row and component represents what was selected.
        let defaults = UserDefaults.standard //UserDefaults()

        if pickerView == self.prayerLanguage {
            defaults.set(languageValues[row], forKey: "prayer_language")
            self.languageChange = true
        } else {
            defaults.set(fontSizeValue[row], forKey: "font_size")
        }
    }
    

    @IBAction func themeChanged(_ sender: Any) {
        let defaults = UserDefaults.standard
        switch theme.selectedSegmentIndex {
        case 0:
            defaults.set(0, forKey: "theme_type")
        case 1:
            defaults.set(1, forKey: "theme_type")
        default:
            break
        }
    }
    
    // MARK: - Navigation

    override func willMove(toParent parent: UIViewController?) {
        super.willMove(toParent: parent)
        if parent == nil {
            let view = self.navigationController!.viewControllers[0] as! ViewController
            if self.languageChange {
                view.languageChanged()
            } else {
                view.reload()
            }
        }
    }
    
}
