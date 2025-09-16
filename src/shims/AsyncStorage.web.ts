// AsyncStorage shim for web using localStorage
// Implements minimal API to match @react-native-async-storage/async-storage

export interface AsyncStorage {
  getItem(key: string): Promise<string | null>;
  setItem(key: string, value: string): Promise<void>;
  removeItem(key: string): Promise<void>;
  clear(): Promise<void>;
}

class WebAsyncStorage implements AsyncStorage {
  async getItem(key: string): Promise<string | null> {
    try {
      return localStorage.getItem(key);
    } catch (error) {
      console.warn('AsyncStorage.getItem error:', error);
      return null;
    }
  }

  async setItem(key: string, value: string): Promise<void> {
    try {
      localStorage.setItem(key, value);
    } catch (error) {
      console.warn('AsyncStorage.setItem error:', error);
      throw error;
    }
  }

  async removeItem(key: string): Promise<void> {
    try {
      localStorage.removeItem(key);
    } catch (error) {
      console.warn('AsyncStorage.removeItem error:', error);
      throw error;
    }
  }

  async clear(): Promise<void> {
    try {
      localStorage.clear();
    } catch (error) {
      console.warn('AsyncStorage.clear error:', error);
      throw error;
    }
  }
}

// Export a singleton instance
export default new WebAsyncStorage(); 